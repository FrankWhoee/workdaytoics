import os

import pandas as pd
import sys
import ics
import datetime
import math

def parseTime(timeStr):
    added = 0
    if "p.m." in timeStr and not "12:" in timeStr:
        added = 12
    timeStr = timeStr.replace(" a.m.", "").replace(" p.m.", "")
    timeStr = timeStr.split(":")
    return datetime.time(hour=int(timeStr[0])+added, minute=int(timeStr[1]))

def printTime(time):
    hour = str(math.floor(time/60))
    minute = str(time%60)
    if len(minute) < 2:
        minute = "0" + minute
    return hour + ":" + minute

if len(sys.argv) > 2:
    print("This tool only takes one argument, which is the filepath.")
    exit(os.EX_USAGE)
elif len(sys.argv) == 1:
    fp = "View_My_Courses.xlsx"
else:
    fp = sys.argv[1]
df = pd.read_excel(fp)

daysOfweek = ["Mon", "Tue", "Wed", "Thu", "Fri"]
schedule = []
for i in range(2):
    term = []
    for d in daysOfweek:
        term.append([])
    schedule.append(term)

for i in range(df.shape[0] -2):
    meetingPattern = df.loc[i+2].iloc[7].split('\n')[0].split("|")
    name = df.loc[i+2].iloc[1].replace("_V", "")
    location = meetingPattern[3][1:]
    time = meetingPattern[2].split(" - ")
    start_time = parseTime(time[0])
    end_time = parseTime(time[1])
    term = 0
    if df.loc[i+2].iloc[10].month != 9:
        term = 1
    for i in range(len(daysOfweek)):
        if daysOfweek[i] in meetingPattern[1]:
            schedule[term][i].append({'name': name, 'start': start_time, 'end': end_time, 'location': location})

for t in schedule:
    for d in t:
        d.sort(key=lambda o: o['start'])

for t in range(len(schedule)):
    print("\nterm " + str(t + 1))
    for d in range(len(schedule[t])):
        print("\n" + daysOfweek[d])
        for c in schedule[t][d]:
            print(c['start'].strftime("%H:%M") + " - " + c['end'].strftime("%H:%M") + "\n" + c['name'] + ", " + c['location'])
    