import pytz
from datetime import datetime, timezone
import time

def dt_to_icsdttz(dt: datetime):
    return dt.strftime('TZID=%Z:%Y%m%dT%H%M%S')
def dt_to_icsdt(dt: datetime):
    return dt.strftime('%Y%m%dT%H%M%S')

def timezonedt(dt: datetime):
    return dt.astimezone()