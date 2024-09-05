
from datetime import datetime, timedelta

from src.constants import xlsx_to_ics_weekday_mapping
from src.iCalendar import iCalendar, Event, RRULE
from src.util import unpack_excel_row, collapse_schedule
import pandas as pd
import os
import csv

buildings = {}

if os.path.isfile("assets/buildingsGeo.csv"):
    with open('assets/buildingsGeo.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            buildings[row[0]] = (float(row[2]),float(row[3]))
else:
    pass

def convert(fp):
    df = pd.read_excel(fp)

    calendar = iCalendar()

    for i in range(2, df.shape[0]):
        row = df.loc[i]

        credits, section, schedule, instructor, start_date, end_date = unpack_excel_row(row)
        schedules = collapse_schedule(schedule)
        for schedule in schedules:
            schedule = schedule.split("|")
            byday = [xlsx_to_ics_weekday_mapping[d] for d in schedule[1].strip().split(" ")]

            dtstartend = schedule[2].split("-")
            dtstart = dtstartend[0].replace(".", "").strip()
            dtend = dtstartend[1].replace(".", "").strip()

            dtstarthours = datetime.strptime(dtstart, "%I:%M %p")
            dtendhours = datetime.strptime(dtend, "%I:%M %p")

            start_date_actual = datetime.fromtimestamp(start_date.timestamp())
            while xlsx_to_ics_weekday_mapping[start_date_actual.strftime("%a")] not in byday:
                start_date_actual += timedelta(days=1)

            dtstart = start_date_actual.replace(hour=dtstarthours.hour, minute=dtstarthours.minute)
            dtend = start_date_actual.replace(hour=dtendhours.hour, minute=dtendhours.minute)

            location = schedule[3]
            description = f"Credits: {credits}\\nInstructor: {instructor}\\nLocation: {location}"
            lat, lon = buildings[location.split("-")[0].strip()]

            rrule = RRULE().weekly().on_days_of_the_week(byday).untilDate(end_date)

            event = Event(dtstart, dtend, section, description, location, lat, lon, rrule)

            calendar.add_event(event)
    return calendar