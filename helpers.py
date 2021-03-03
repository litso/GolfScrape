from datetime import datetime, timedelta
from pytz import timezone

def nextSaturday(d=datetime.now()):
	t = timedelta((7 + 5 - d.weekday()) % 7)
	return (d + t).strftime('%m/%d/%Y')

def time_in_los_angeles():
	tz = timezone("America/Los_Angeles")
	return datetime.now(tz)

def results_filename(d=time_in_los_angeles()):
	return "rancho_park-" + d.astimezone().isoformat() + ".json"
