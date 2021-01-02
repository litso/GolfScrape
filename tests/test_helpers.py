import unittest

from datetime import datetime

from helpers import Date

class HelperTest(unittest.TestCase):

  def test_next_saturday(self):
	  # January 1st was a Friday
	  startdate = "01-01-2021"
	  d = datetime.strptime(startdate, '%m-%d-%Y')

	  x = Date().nextSaturday()
	  self.assertEqual(x, "01-02-2021")