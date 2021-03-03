import unittest

from datetime import datetime
from pytz import timezone

from helpers import *

class HelperTest(unittest.TestCase):

  def test_next_saturday(self):
	  # January 1st was a Friday
	  startdate = "01-01-2021"
	  friday = datetime.strptime(startdate, '%m-%d-%Y')

	  saturday = nextSaturday(friday)
	  self.assertEqual(saturday, "01/02/2021")

  def test_file_name(self):
	  tz = timezone("America/Los_Angeles")

	  startdate = "01-01-2021"
	  friday = datetime.strptime(startdate, '%m-%d-%Y')
	  friday.replace(tzinfo=tz)

	  result = results_filename(friday)
	  self.assertEqual(result, "rancho_park-2021-01-01T00:00:00-08:00")

  def test_time_in_los_angeles(self):
	  time = time_in_los_angeles()
	  self.assertEqual(time.tzinfo.zone, 'America/Los_Angeles')
