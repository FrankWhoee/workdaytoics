import uuid
from src.util import dt_to_icsdttz, timezonedt, dt_to_icsdt
from datetime import datetime

class icsComponent:

    def to_ics(self):
        pass

class RRULE(icsComponent):

    def __init__(self, freq=None, interval=None, byday=None, until=None):
        self.freq = freq
        self.byday = byday
        self.until = until
        self.interval = interval
        self.byday = byday
    
    def happens(self, interval: int):
        self.interval = interval
        return self
    
    def every(self, freq: str):
        self.freq = freq
        return self

    def daily(self):
        self.freq = "DAILY"
        return self
    def weekly(self):
        self.freq = "WEEKLY"
        return self

    def monthly(self):
        self.freq = "MONTHLY"
        return self

    def yearly(self):
        self.freq = "YEARLY"
        return self

    def on_days_of_the_week(self, days_of_week):
        self.byday = days_of_week
        return self

    def untilDate(self, dt: datetime):
        self.until = dt
        return self
    
    def to_ics(self):
        output = ""

        if self.freq:
            output += f"FREQ={self.freq};"

        if self.interval:
            output += f"INTERVAL={str(self.interval)};"

        if self.byday:
            output += f"BYDAY={','.join(self.byday)};"

        if self.until:
            output += f"UNTIL={dt_to_icsdt(self.until)};"
        
        return output


class Event(icsComponent):

    def __init__(self, dtstart: datetime, dtend, summary, description, location, lat, lon, rrule):
        self.uid = str(uuid.uuid4())
        self.dtstamp = dt_to_icsdttz(timezonedt(datetime.now()))
        self.dtstart = timezonedt(dtstart)
        self.dtend = timezonedt(dtend)
        self.summary = summary
        self.description = description
        self.location = location
        self.lat = lat
        self.lon = lon
        self.rrule = rrule

    def to_ics(self):
        output = "BEGIN:VEVENT\n"

        output += f"UID:{self.uid}\n"
        output += f"DTSTAMP;{self.dtstamp}\n"
        output += f"DTSTART;{dt_to_icsdttz(self.dtstart)}\n"
        output += f"DTEND;{dt_to_icsdttz(self.dtend)}\n"
        output += f"SUMMARY:{self.summary}\n"

        if self.description:
            output += f"DESCRIPTION:{self.description};\n"

        if self.location:
            output += f"LOCATION:{self.location}\n"

        if self.lat and self.lon:
            output += f"GEO:{self.lat};{self.lon}\n"

        if self.rrule:
            output += "RRULE:" + self.rrule.to_ics() + "\n"

        output += f"END:VEVENT\n"

        return output

class iCalendar(icsComponent):

    def __init__(self):
        self.events = []

    def add_event(self, event: Event):
        self.events.append(event)

    def to_ics(self):
        output = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:" + str(uuid.uuid4()) +"\n"
        for e in self.events:
            output += e.to_ics()
        output += "END:VCALENDAR"

        return output