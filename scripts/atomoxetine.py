# Whatsapp notifications doesn't seem that good cause there are some days when I'm not online. I will implement a way to do it using push notifications peraphs on pc and phone. 
# In the meantime this is good enough
# This program is very brittle though
# If you're useful, I promise to improve you
from datetime import timedelta, datetime, date
import os
import pywhatkit
import pickle
from dotenv import load_dotenv
import sys

load_dotenv()
NATHAN_NUM = os.environ.get("NATHAN_NUM")
today = datetime.now().date()


class PillStock:
    def __init__(self, dosePerPill: int, prescribedDose: int, stock: int, splitDose: bool):
        self.dosePerPill = dosePerPill
        self.prescribedDose = prescribedDose
        self.stock = stock
        self.numberOfPillsPerDay: float = self.prescribedDose / self.dosePerPill
        self.numberOfDaysCovered = self.stock / self.numberOfPillsPerDay
        self.dateWhenStockEnds = datetime.now() + timedelta(days=self.numberOfDaysCovered)
        self.numberOfDosesTakenToday: int = 0
        self.splitDose = splitDose
        self.lastFullDose: date = None

    def _resetIfNewDay(self):
        if self.lastFullDose != today:
            self.numberOfDosesTakenToday = 0

    def _markFullDoseIfComplete(self):
        if self.splitDose and self.numberOfDosesTakenToday == 2:
            self.lastFullDose = today
        elif not self.splitDose and self.numberOfDosesTakenToday == 1:
            self.lastFullDose = today

    def updateStock(self):
        if self.splitDose:
            self.stock -= self.numberOfPillsPerDay / 2
        else:
            self.stock -= self.numberOfPillsPerDay

    def recompute(self):
        self.numberOfDaysCovered = self.stock / self.numberOfPillsPerDay
        self.dateWhenStockEnds = datetime.now() + timedelta(days=self.numberOfDaysCovered)

    def drinkMeds(self):
        self._resetIfNewDay()

        if self.lastFullDose == today:
            print("Already completed today's dose.")
            return

        if self.splitDose and self.numberOfDosesTakenToday in (0, 1):
            pywhatkit.sendwhatmsg_instantly(
                NATHAN_NUM,
                f'Nathan drink {self.numberOfPillsPerDay / 2} pills',
                10
            )
            self.numberOfDosesTakenToday += 1
            self.updateStock()
            self.recompute()
            self._markFullDoseIfComplete()

        elif not self.splitDose and self.numberOfDosesTakenToday == 0:
            pywhatkit.sendwhatmsg_instantly(
                NATHAN_NUM,
                f'Nathan drink {self.numberOfPillsPerDay} pills',
                10
            )
            self.numberOfDosesTakenToday += 1
            self.updateStock()
            self.recompute()
            self._markFullDoseIfComplete()

    def status(self):
        print(f'Stock remaining: {self.stock} pills')
        print(f'Days covered: {self.numberOfDaysCovered:.1f}')
        print(f'Stock ends: {self.dateWhenStockEnds.strftime("%Y-%m-%d")}')
        print(f'Doses taken today: {self.numberOfDosesTakenToday}')
        print(f'Last full dose: {self.lastFullDose}')
        print(f'Split dose {self.splitDose}')


arg = sys.argv[1] if len(sys.argv) > 1 else None

if arg == "init":
    atomoxetine = PillStock(
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        bool(sys.argv[5])
    )
    with open("atomoxetine.pkl", "wb") as f:
        pickle.dump(atomoxetine, f)
    print("Initialized and saved.")
    exit()

with open("atomoxetine.pkl", "rb") as f:
    atomoxetine = pickle.load(f)

if sys.argv[1]== "status":
    atomoxetine.status()
else:
    atomoxetine.drinkMeds()
    with open("atomoxetine.pkl", "wb") as f:
        pickle.dump(atomoxetine, f)
