from datetime import datetime, timedelta

class Date:
	def nextSaturday(self, d=datetime.now()):
		t = timedelta((7 + 5 - d.weekday()) % 7)
		return (d + t).strftime('%m-%d-%Y')
