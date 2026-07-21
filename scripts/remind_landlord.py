from datetime import timedelta, datetime
import pickle
import os
import sys
from dotenv import load_dotenv

load_dotenv()

AROKIUM_NUM = os.environ.get("AROKIUM_NUM")
AROKIUM_MSG = os.environ.get("AROKIUM_MSG").replace("\\n", "\n")
NATHAN_NUM = os.environ.get("NATHAN_NUM")
NTFY_TOPIC= os.environ.get("NTFY_TOPIC")

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
            import pywhatkit
            import requests
            self.status = 'waiting'
            pywhatkit.sendwhatmsg_instantly(AROKIUM_NUM, AROKIUM_MSG, 10)
            requests.post(NTFY_TOPIC,AROKIUM_MSG)
            self.updateDueDate()

    def moneyReceived(self):
        self.status = sys.argv[1]
        self.updateDueDate()

def loadOrCreate():
    if os.path.exists("nathan.pkl"):
        with open("/home/nathan/.local/share/nathan.pkl", "rb") as f:
            return pickle.load(f)
    elif sys.argv[1] == "waiting":
        return Scheduler('waiting')
    else:
        return Scheduler(status='received', lastDateSent=datetime.now())

def updateLastDateSent(self,day):
    self.lastDateSent = day
    self.dueDate = day + self.interval


    
arg = sys.argv[1] if len(sys.argv) > 1 else None
nathan = loadOrCreate()

if arg == 'received':
    nathan.moneyReceived()
else if arg == 'update':
    nathan.updateLastDateSent()
    nathan.statusChange()



with open("/home/nathan/.local/share/nathan.pkl", "wb") as f:
    pickle.dump(nathan, f)
