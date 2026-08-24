#!/usr/bin/env python3
"""
nathan-scheduler
================

Recurring payment reminder scheduler backed by SQLite.

Tracks a single recurring due date (interval: 29 days, 7 hours).

Commands
--------
    scheduler.py
        Check whether the current due date has passed.
        If it has, send the reminder and schedule the next due date.

    scheduler.py received
        Mark the payment as received now and schedule the next due date.
        Does NOT send a reminder.

    scheduler.py update
        Reset lastDateSent to now, calculate a new due date, and check
        whether that newly calculated due date has already passed.

    scheduler.py update 2026-08-15
        Set lastDateSent to the specified date, calculate the new due date,
        and check whether that newly calculated due date has already passed.

State
-----
    ~/.local/share/nathan-scheduler/scheduler.db

Environment variables
---------------------
    AROKIUM_NUM
        WhatsApp number to send the reminder to.

    AROKIUM_MSG
        Reminder message. Literal "\\n" is converted to a newline.

    NATHAN_NUM
        Reserved for future use.

    NTFY_TOPIC
        Full ntfy.sh topic URL.

Examples
--------
    scheduler.py
    scheduler.py received
    scheduler.py update
    scheduler.py update 2026-08-15

Exit codes
----------
    0   Success
    2   Bad command-line input
    1   Runtime/notification error
"""

import argparse
import os
import sqlite3
from datetime import datetime, timedelta

from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

AROKIUM_NUM = os.environ.get("AROKIUM_NUM")
AROKIUM_MSG = os.environ.get("AROKIUM_MSG", "").replace("\\n", "\n")
NATHAN_NUM = os.environ.get("NATHAN_NUM")  # Reserved for future use.
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

DATA_DIR = os.path.expanduser("~/.local/share/nathan-scheduler")
DB_PATH = os.path.join(DATA_DIR, "scheduler.db")

DATE_FMT = "%Y-%m-%d %H:%M:%S.%f"
DATE_ARG_FMT = "%Y-%m-%d"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def get_connection():
    """Open the SQLite database and create tables if necessary."""
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
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


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User:
    """Represents a user stored in the database."""

    def __init__(self, name, conn=None, id=None):
        self.name = name
        self.id = id

        if self.id is None and conn is not None:
            cur = conn.execute(
                "SELECT id FROM users WHERE name = ?",
                (name,)
            )
            row = cur.fetchone()

            if row:
                self.id = row[0]
            else:
                cur = conn.execute(
                    "INSERT INTO users (name) VALUES (?)",
                    (name,)
                )
                conn.commit()
                self.id = cur.lastrowid

    def getId(self):
        return self.id


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """Manage the single recurring payment schedule."""

    interval = timedelta(days=29, hours=7)

    def __init__(
        self,
        user,
        status=None,
        lastDateSent=None,
        dueDate=None,
    ):
        self.status = status
        self.lastDateSent = lastDateSent or datetime.now()
        self.dueDate = dueDate or (
            self.lastDateSent + self.interval
        )
        self.userId = user.getId()

    # -----------------------------------------------------------------------
    # Date handling
    # -----------------------------------------------------------------------

    def updateDueDate(self):
        """
        Reset the schedule from now.

        The exact same timestamp is used as the base for both values.
        """
        now = datetime.now()
        self.lastDateSent = now
        self.dueDate = now + self.interval

    def updateLastDateSent(self, day=None):
        """
        Set lastDateSent to a supplied datetime or now, then calculate
        the corresponding due date.
        """
        self.lastDateSent = day or datetime.now()
        self.dueDate = self.lastDateSent + self.interval

    # -----------------------------------------------------------------------
    # Reminder handling
    # -----------------------------------------------------------------------

    def sendReminder(self):
        """Send the WhatsApp and ntfy notifications."""
        if not AROKIUM_NUM:
            raise RuntimeError(
                "AROKIUM_NUM is not set in the environment."
            )

        if not AROKIUM_MSG:
            raise RuntimeError(
                "AROKIUM_MSG is not set in the environment."
            )

        if not NTFY_TOPIC:
            raise RuntimeError(
                "NTFY_TOPIC is not set in the environment."
            )

        import pywhatkit
        import requests

        # WhatsApp reminder.
        pywhatkit.sendwhatmsg_instantly(
            AROKIUM_NUM,
            AROKIUM_MSG,
            10,
        )

        # ntfy reminder.
        response = requests.post(
            NTFY_TOPIC,
            data=AROKIUM_MSG.encode("utf-8"),
            timeout=15,
        )

        response.raise_for_status()

    def statusChange(self):
        """
        Check the current due date.

        If dueDate has passed:
            - send the reminder
            - mark status as waiting
            - roll the schedule forward from now

        Otherwise, do nothing.
        """
        now = datetime.now()

        if now < self.dueDate:
            return False

        # The payment is overdue, so send the reminder.
        self.sendReminder()

        self.status = "waiting"
        self.updateDueDate()

        return True

    def moneyReceived(self):
        """
        Mark payment as received now.

        This never sends a reminder.
        """
        self.status = "received"
        self.updateDueDate()

    # -----------------------------------------------------------------------
    # Persistence
    # -----------------------------------------------------------------------

    def save(self, conn):
        """Save current scheduler state to SQLite."""
        conn.execute("""
            INSERT INTO scheduler (
                id,
                status,
                lastDateSent,
                dueDate,
                userId
            )
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
        """Load the scheduler state from SQLite."""
        cur = conn.execute("""
            SELECT status, lastDateSent, dueDate, userId
            FROM scheduler
            WHERE id = 1
        """)

        row = cur.fetchone()

        if row is None:
            return None

        status, lastDateSent, dueDate, userId = row

        user = User(
            name="Nathan",
            conn=conn,
            id=userId,
        )

        return cls(
            user,
            status=status,
            lastDateSent=datetime.strptime(
                lastDateSent,
                DATE_FMT,
            ),
            dueDate=datetime.strptime(
                dueDate,
                DATE_FMT,
            ),
        )


# ---------------------------------------------------------------------------
# Loading / initialization
# ---------------------------------------------------------------------------

def loadOrCreate(conn):
    """Load existing scheduler or create a new one."""
    existing = Scheduler.load(conn)

    if existing is not None:
        return existing

    user = User("Nathan", conn=conn)

    # First run:
    # payment is considered received now, so the first due date is
    # now + 29 days + 7 hours.
    scheduler = Scheduler(
        user,
        status="received",
    )

    scheduler.save(conn)

    return scheduler


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    """Construct the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="scheduler.py",
        description=(
            "Recurring payment reminder scheduler "
            "(SQLite-backed)."
        ),
        epilog=(
            "Examples:\n"
            "  scheduler.py\n"
            "      Check the existing due date.\n\n"

            "  scheduler.py received\n"
            "      Mark payment as received now and reset the due date.\n\n"

            "  scheduler.py update\n"
            "      Set lastDateSent to now, calculate a new due date,\n"
            "      and check whether that new due date has passed.\n\n"

            "  scheduler.py update 2026-08-15\n"
            "      Set lastDateSent to the specified date, calculate\n"
            "      the new due date, and check whether it has passed."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "received",
        help=(
            "Mark payment as received now and reset the due date. "
            "Does not send a reminder."
        ),
    )

    update_parser = subparsers.add_parser(
        "update",
        help=(
            "Recalculate the due date from a new lastDateSent value "
            "and check whether the new due date has passed."
        ),
    )

    update_parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help=(
            "Optional date in YYYY-MM-DD format. "
            "Defaults to now."
        ),
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    conn = get_connection()

    try:
        scheduler = loadOrCreate(conn)

        # ---------------------------------------------------------------
        # received
        # ---------------------------------------------------------------
        if args.command == "received":
            scheduler.moneyReceived()
            scheduler.save(conn)

            print(
                "Marked as received.\n"
                f"Last payment: {scheduler.lastDateSent}\n"
                f"Next due date: {scheduler.dueDate}"
            )

        # ---------------------------------------------------------------
        # update
        # ---------------------------------------------------------------
        elif args.command == "update":
            day = None

            if args.date is not None:
                try:
                    day = datetime.strptime(
                        args.date,
                        DATE_ARG_FMT,
                    )
                except ValueError:
                    parser.error(
                        f"invalid date '{args.date}', "
                        f"expected format YYYY-MM-DD "
                        f"(e.g. 2026-08-15)"
                    )

            # First calculate the NEW due date.
            scheduler.updateLastDateSent(day)

            print(
                f"Last payment date: {scheduler.lastDateSent}\n"
                f"New due date:      {scheduler.dueDate}"
            )

            # Then check ONLY this newly calculated due date.
            reminder_sent = scheduler.statusChange()

            if reminder_sent:
                print("New due date has already passed. Reminder sent.")
            else:
                print("New due date has not passed. No reminder sent.")

            scheduler.save(conn)

        # ---------------------------------------------------------------
        # no command
        # ---------------------------------------------------------------
        else:
            reminder_sent = scheduler.statusChange()

            if reminder_sent:
                print("Due date passed. Reminder sent.")
            else:
                print(
                    f"Not due yet. Due date: {scheduler.dueDate}"
                )

            scheduler.save(conn)

    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
