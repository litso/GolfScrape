from datetime import datetime, timedelta

def nextSaturday(d=datetime.now()):
	t = timedelta((7 + 5 - d.weekday()) % 7)
	return (d + t).strftime('%m-%d-%Y')
