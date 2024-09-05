import pytz
from datetime import datetime, timezone
import time

def dt_to_icsdttz(dt: datetime):
    return dt.strftime('TZID=America/Vancouver:%Y%m%dT%H%M%S')
def dt_to_icsdt(dt: datetime):
    return dt.strftime('%Y%m%dT%H%M%S')

def timezonedt(dt: datetime):
    return dt.astimezone()

def unpack_excel_row(row):
    credits = row.iloc[2]
    section = row.iloc[4]
    schedule = row.iloc[7]
    instructor = row.iloc[9]
    start_date = row.iloc[10]
    end_date = row.iloc[11]

    return (credits, section, schedule, instructor, start_date, end_date)

def collapse_schedule(schedule):
    schedule = schedule.split("\n")
    output_schedule = {}
    for s in schedule:
        if s:
            data = s.split("|")
            weekdays = data[1]
            times = data[2]
            loc = data[3]
            output_schedule[weekdays + times + loc] = s

    return list(output_schedule.values())