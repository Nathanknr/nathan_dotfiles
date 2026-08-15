#!/usr/bin/env python3
"""
nathan-scheduler
================

Recurring payment reminder scheduler backed by SQLite.

Tracks a single recurring due date (interval: 29 days, 7 hours). When the
due date passes, sends a WhatsApp message (via pywhatkit) and an ntfy.sh
push notification, then rolls the due date forward. Intended to be run
periodically (e.g. from a cron job or systemd timer) with no arguments,
and manually with 'received' or 'update' when state needs to change.

State is stored in:
    ~/.local/share/nathan-scheduler/scheduler.db

Environment variables (loaded from a .env file in the working directory):
    AROKIUM_NUM   WhatsApp number to send the reminder to
    AROKIUM_MSG   Reminder message text (use literal \\n for newlines)
    NATHAN_NUM    (reserved, currently unused by the script logic)
    NTFY_TOPIC    Full ntfy.sh topic URL to POST the reminder to

Usage
-----
    scheduler.py                       Check if due date has passed; if so,
                                        send the reminder and roll the date
                                        forward. No-op otherwise. This is the
                                        command to run on a schedule.

    scheduler.py received              Mark payment as received right now
                                        and reset the due date to
                                        now + interval.

    scheduler.py update                Reset lastDateSent to right now and
                                        recompute the due date from it.

    scheduler.py update 2026-08-15     Set lastDateSent to a specific date
                                        (format: YYYY-MM-DD) and recompute
                                        the due date from it.

Exit codes
----------
    0   Success
    2   Bad input (e.g. invalid date format, unrecognized command)

Examples
--------
    # Run silently from a systemd timer / cron every few hours:
    $ scheduler.py

    # Nathan tells the script the payment came in today:
    $ scheduler.py received

    # Backdate the last payment to a specific day (e.g. correcting a
    # missed run):
    $ scheduler.py update 2026-08-15
"""

import argparse
import os
import sqlite3
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()
AROKIUM_NUM = os.environ.get("AROKIUM_NUM")
AROKIUM_MSG = os.environ.get("AROKIUM_MSG").replace("\\n", "\n")
NATHAN_NUM = os.environ.get("NATHAN_NUM")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

DATA_DIR = os.path.expanduser("~/.local/share/nathan-scheduler")
DB_PATH = os.path.join(DATA_DIR, "scheduler.db")

# Format used to store datetimes in SQLite (which has no native datetime type).
DATE_FMT = "%Y-%m-%d %H:%M:%S.%f"
# Format accepted from the user on the command line (date only, no time).
DATE_ARG_FMT = "%Y-%m-%d"


def get_connection():
    """
    Open (creating if necessary) the scheduler's SQLite database.

    Creates DATA_DIR and the 'users' / 'scheduler' tables on first run.
    Safe to call every time the script runs; existing data is left as-is.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scheduler (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            status TEXT,
            lastDateSent TEXT NOT NULL,
            dueDate TEXT NOT NULL,
            userId INTEGER,
            FOREIGN KEY (userId) REFERENCES users(id)
        )
    """)
    conn.commit()
    return conn


class User:
    """A named user, looked up or created in the 'users' table."""

    def __init__(self, name, conn=None, id=None):
        """
        Args:
            name: Display name for the user.
            conn: Open sqlite3 connection. If given and id is None, looks
                up the user by name, creating a row if none exists.
            id: Known user id (skips the DB lookup/creation above).
        """
        self.name = name
        self.id = id
        if self.id is None and conn is not None:
            cur = conn.execute("SELECT id FROM users WHERE name = ?", (name,))
            row = cur.fetchone()
            if row:
                self.id = row[0]
            else:
                cur = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
                conn.commit()
                self.id = cur.lastrowid

    def getId(self):
        return self.id


class Scheduler:
    """
    Tracks a single recurring due date for one user.

    The single row of state lives in the 'scheduler' table (id fixed at 1),
    since this script only ever tracks one schedule at a time.
    """

    interval = timedelta(days=29, hours=7)

    def __init__(self, user, status=None, lastDateSent=None, dueDate=None):
        self.status = status
        self.lastDateSent = lastDateSent or datetime.now()
        self.dueDate = dueDate or (self.lastDateSent + self.interval)
        self.userId = user.getId()

    def updateDueDate(self):
        """Reset lastDateSent to now and push dueDate forward by interval."""
        self.lastDateSent = datetime.now()
        self.dueDate = datetime.now() + self.interval

    def updateLastDateSent(self, day=None):
        """
        Set lastDateSent to a specific datetime (or now, if none given)
        and recompute dueDate from it.
        """
        self.lastDateSent = day or datetime.now()
        self.dueDate = self.lastDateSent + self.interval

    def statusChange(self):
        """
        Check whether the due date has passed. If it has, send the
        WhatsApp reminder and ntfy notification, mark status as
        'waiting', and roll the due date forward. No-op if the due
        date hasn't arrived yet, or if already waiting and not yet due.
        """
        if self.status == 'waiting' and datetime.now() < self.dueDate:
            return
        elif datetime.now() >= self.dueDate:
            import pywhatkit
            import requests
            self.status = 'waiting'
            pywhatkit.sendwhatmsg_instantly(AROKIUM_NUM, AROKIUM_MSG, 10)
            requests.post(NTFY_TOPIC, AROKIUM_MSG)
            self.updateDueDate()

    def moneyReceived(self, status):
        """Mark payment as received and reset the due date."""
        self.status = status
        self.updateDueDate()

    def save(self, conn):
        """Persist current state to the 'scheduler' table (upsert)."""
        conn.execute("""
            INSERT INTO scheduler (id, status, lastDateSent, dueDate, userId)
            VALUES (1, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status,
                lastDateSent = excluded.lastDateSent,
                dueDate = excluded.dueDate,
                userId = excluded.userId
        """, (
            self.status,
            self.lastDateSent.strftime(DATE_FMT),
            self.dueDate.strftime(DATE_FMT),
            self.userId,
        ))
        conn.commit()

    @classmethod
    def load(cls, conn):
        """Load existing state from the 'scheduler' table, or None if absent."""
        cur = conn.execute("SELECT status, lastDateSent, dueDate, userId FROM scheduler WHERE id = 1")
        row = cur.fetchone()
        if row is None:
            return None
        status, lastDateSent, dueDate, userId = row
        user = User(name="Nathan", conn=conn, id=userId)
        return cls(
            user,
            status=status,
            lastDateSent=datetime.strptime(lastDateSent, DATE_FMT),
            dueDate=datetime.strptime(dueDate, DATE_FMT),
        )


def loadOrCreate(conn, initial_status=None):
    """
    Load the existing Scheduler from the database, or create a fresh one
    if this is the first run.

    Args:
        conn: Open sqlite3 connection.
        initial_status: Status to use only when creating a brand-new
            Scheduler (ignored if one already exists in the database).
    """
    existing = Scheduler.load(conn)
    if existing is not None:
        return existing

    user = User("Nathan", conn=conn)
    if initial_status == "waiting":
        return Scheduler(user, status='waiting')
    else:
        return Scheduler(user, status='received', lastDateSent=datetime.now())


def build_parser():
    """Construct the argparse CLI parser with subcommands and help text."""
    parser = argparse.ArgumentParser(
        prog="scheduler.py",
        description="Recurring payment reminder scheduler (SQLite-backed).",
        epilog=(
            "Examples:\n"
            "  scheduler.py                     Check due date, send reminder if due\n"
            "  scheduler.py received            Mark payment as received now\n"
            "  scheduler.py update              Reset last-sent date to now\n"
            "  scheduler.py update 2026-08-15   Set last-sent date to a specific day\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "received",
        help="Mark payment as received now and reset the due date.",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Reset the last-sent date (to now, or to a given day) and re-check due date.",
    )
    update_parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help=f"Optional date in {DATE_ARG_FMT.replace('%', '%%')} format (e.g. 2026-08-15). "
             "Defaults to right now if omitted.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    conn = get_connection()
    nathan = loadOrCreate(conn, initial_status=args.command)

    if args.command == 'received':
        nathan.moneyReceived(args.command)
        print("Marked as received. Due date reset.")
    elif args.command == 'update':
        day = None
        if args.date is not None:
            try:
                day = datetime.strptime(args.date, DATE_ARG_FMT)
            except ValueError:
                parser.error(
                    f"invalid date '{args.date}', expected format {DATE_ARG_FMT} (e.g. 2026-08-15)"
                )
        nathan.updateLastDateSent(day)
        nathan.statusChange()
        print(f"Last-sent date updated to {nathan.lastDateSent}. "
              f"Due date is now {nathan.dueDate}.")
    else:
        nathan.statusChange()

    nathan.save(conn)
    conn.close()


if __name__ == "__main__":
    main()
