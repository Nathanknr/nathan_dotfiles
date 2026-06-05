from datetime import timedelta, datetime
import pickle
import os
import sys
import pywhatkit
from dotenv import load_dotenv

load_dotenv()

AROKIUM_NUM = os.environ.get("AROKIUM_NUM")
AROKIUM_MSG = os.environ.get("AROKIUM_MSG").replace("\\n", "\n")
NATHAN_NUM = os.environ.get("NATHAN_NUM")

class Scheduler:
    interval = timedelta(days=29, hours=7)

    def __init__(self, status=None, lastDateSent=datetime.now()):
        self.status = status
        self.lastDateSent = lastDateSent
        self.dueDate = lastDateSent + self.interval

    def updateDueDate(self):
        self.lastDateSent = datetime.now()
        self.dueDate = datetime.now() + self.interval

    def statusChange(self):
        if self.status == 'waiting' and datetime.now() < self.dueDate:
            return
        elif datetime.now() >= self.dueDate:
            self.status = 'waiting'
            pywhatkit.sendwhatmsg_instantly(AROKIUM_NUM, AROKIUM_MSG, 10)
            self.updateDueDate()

    def moneyReceived(self):
        self.status = sys.argv[1]
        self.updateDueDate()

def loadOrCreate():
    if os.path.exists("nathan.pkl"):
        with open("nathan.pkl", "rb") as f:
            return pickle.load(f)
    elif sys.argv[1] == "waiting":
        return Scheduler('waiting')
    else:
        return Scheduler(status='received', lastDateSent=datetime.now())

arg = sys.argv[1] if len(sys.argv) > 1 else None
nathan = loadOrCreate()

if arg == 'received':
    nathan.moneyReceived()
else:
    nathan.statusChange()



with open("nathan.pkl", "wb") as f:
    pickle.dump(nathan, f)
