# This script will do some things
# This scripts knows how much atomoxetine I have remaining

# This script reminds me on whatsapp to drink my meds

# This script update the atomoxetine count each time it send a message
# This script tells me the number of pills in the solely opened box assuming that I drank it

from datetime import timedelta, datetime

class PillStock:
    def __init__(self, dosePerPill, prescribedDose, stock, splitDose):
        self.dosePerPill = dosePerPill
        self.prescribedDose = prescribedDose
        self.stock = stock
        self.numberOfPillsPerDay = prescribedDose / dosePerPill
        self.numberOfDaysCovered = stock / self.numberOfPillsPerDay
        self.dateWhenStockEnds = datetime.now() + timedelta(days=self.numberOfDaysCovered)
        self.splitDose = splitDose


