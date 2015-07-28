from mileage import mileage
import math
import sys

'''
@params: takes two lat/lon pairs (start and end points)
		 wheelchair = True if passenger is needs accomodations
@returns: the maximum possible taxi cost for a trip with specified 
		  params in dollars 
'''
def taxiCost(lat1, lon1, lat2, lon2, wheelchair):
	# converts from miles to meters and ceilings to nearest decimal
	miles = math.ceil(mileage(lat1, lon1, lat2, lon2) / 160.934) / 10
	cost = sys.maxint

	if wheelchair:
		if miles < 16.67: # Northwest is most expensive
			cost = 21 + miles * 3.5
		elif miles < 61: # Sunshine is most expensive
			cost = 20 + miles * 3.56
		else: # Transpo is most expensive
			cost = 18.78 + miles * 3.58
	else: 
		if miles < 2.14: # Farwest is most expensive
			cost = 3 + miles * 2.6
		else: # Northwest is most expensive
			cost = miles * 4
	return cost

# testing purposes
def main():
	print(taxiCost(47.602558, -122.142807, 47.631370, -122.142979, False))
	print(taxiCost(47.602558, -122.142807, 47.631370, -122.142979, True))

if __name__ == "__main__":
	main()