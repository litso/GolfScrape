import unittest

from datetime import datetime

from helpers import *

class HelperTest(unittest.TestCase):

  def test_next_saturday(self):
	  # January 1st was a Friday
	  startdate = "01-01-2021"
	  friday = datetime.strptime(startdate, '%m-%d-%Y')

	  saturday = nextSaturday(friday)
	  self.assertEqual(saturday, "01-02-2021")