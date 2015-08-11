import unittest
import travelCosts
import timeConversion

class unit_tests(unittest.TestCase):

	def test_taxi_cost(self):
		self.assertEqual(travelCosts.taxi(47.602558, -122.142807, 47.631370, -122.142979, False), 8.20)
		self.assertEqual(travelCosts.taxi(47.602558, -122.142807, 47.631370, -122.142979, True), 28.00)

	def newBusRun_test(self):
		pass

	def timeConversion_test(self):
		self.assertEqual(timeConversion.secondsToHuman(timeConversion.humanToSeconds('12:37')), '12:37')
		

if __name__ == '__main__':
    unittest.main()