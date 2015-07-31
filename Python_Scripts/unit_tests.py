import unittest
import travelCosts

class unit_tests(unittest.TestCase):

	def test_taxi_cost(self):
		self.assertEqual(travelCosts.taxi(47.602558, -122.142807, 47.631370, -122.142979, False), 8.20)
		self.assertEqual(travelCosts.taxi(47.602558, -122.142807, 47.631370, -122.142979, True), 28.00)

if __name__ == '__main__':
    unittest.main()