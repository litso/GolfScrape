import unittest

from datetime import datetime
from dateutil import tz, parser

from helpers import *

class HelperTest(unittest.TestCase):

  def test_next_saturday(self):
      # January 1st was a Friday
      startdate = "01-01-2021"
      friday = datetime.strptime(startdate, '%m-%d-%Y')

      saturday = nextSaturday(friday)
      self.assertEqual(saturday, "01/02/2021")

  def test_file_name(self):
      time_zone = tz.gettz("America/Los_Angeles")
      friday = datetime(2021, 1, 1, 0, tzinfo=time_zone)

      friday_in_system_tz = friday.astimezone().isoformat() 

      result = results_filename(friday)
      self.assertEqual(
        result, 
        'rancho_park-{}.json'.format(friday.astimezone().isoformat())
      )

  def test_time_in_los_angeles(self):
      time = time_in_los_angeles()
      print(dir(time.tzinfo))
      name = time.tzinfo.tzname(time)

      if "PD" in name:
          self.assertEqual(
             name, 
             'PDT'
           )
      else:
           self.assertEqual(
              name, 
              'PST'
            )
