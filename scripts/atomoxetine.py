# This script will do some things
# This scripts knows how much atomoxetine I have remaining
# This script reminds me on whatsapp to drink my meds
# This script update the atomoxetine count each time it send a message
# This script tells me the number of pills in the solely opened box assuming that I drank it
from datetime import timedelta, datetime
import os
import pywhatkit
from dotenv import load_dotenv

load_dotenv()
NATHAN_NUM = os.environ.get("NATHAN_NUM")

class PillStock:
    def __init__(self, dosePerPill, prescribedDose, stock, splitDose):
        self.dosePerPill = dosePerPill
        self.prescribedDose = prescribedDose
        self.stock = stock
        self.numberOfPillsPerDay = prescribedDose / dosePerPill
        self.numberOfDaysCovered = stock / self.numberOfPillsPerDay
        self.dateWhenStockEnds = datetime.now() + timedelta(days=self.numberOfDaysCovered)
        self.numberOfDosesTakenToday = 0
        self.splitDose = splitDose

    def updateStock(self):
        if self.splitDose:
            self.stock = self.stock - self.numberOfPillsPerDay / 2
        else:
            self.stock = self.stock - self.numberOfPillsPerDay

    def recompute(self):
        self.numberOfDaysCovered = self.stock / self.numberOfPillsPerDay
        self.dateWhenStockEnds = datetime.now() + timedelta(days=self.numberOfDaysCovered)

    def drinkMeds(self):
        if self.splitDose and self.numberOfDosesTakenToday in (0, 1):
            pywhatkit.sendwhatmsg_instantly(NATHAN_NUM, f'Nathan drink {self.numberOfPillsPerDay / 2} pills', 10)
            self.numberOfDosesTakenToday += 1
            self.updateStock()
            self.recompute()
        elif not self.splitDose and self.numberOfDosesTakenToday == 0:
            pywhatkit.sendwhatmsg_instantly(NATHAN_NUM, f'Nathan drink {self.numberOfPillsPerDay} pills', 10)
            self.numberOfDosesTakenToday += 1
            self.updateStock()
            self.recompute()
