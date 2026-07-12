import sqlite3
from datetime import date
import re
# Connect to dbk
con = sqlite3.connect("/home/nathan/.local/share/problem_db/problem.db")

today = date.today().isoformat()
# add one problem to db

def addProblem(difficulty, hint, day):
    con.execute(
        "INSERT INTO problem (difficulty, hint, date) VALUES (?,?,?)",
        (int(difficulty), int(hint), day)
    )

def addProblemToday(difficulty, hint):
    addProblem(difficulty, hint, today)


# This function will take a text file and parse each will with int,int and add it to db
def bulkAddProblemToday(text_file):
    with open(text_file,'r') as file:
        text = file.read()
        object = re.compile(r'([0-9]),([0-9])\n')
        match = object.findall(text)
        for i in range(0,len(match)):
            difficulty = match[i][0]
            hint = match[i][1]
            addProblemToday(difficulty,hint)
        con.commit()


def bulkAddProblem(text_file, day):
        with open(text_file,'r') as file:
            text = file.read()
            object = re.compile(r'([0-9]),([0-9])\n')
            match = object.findall(text)
            for i in range(0,len(match)):
                difficulty = match[i][0]
                hint = match[i][1]
                addProblem(difficulty,hint,day)
            con.commit()
