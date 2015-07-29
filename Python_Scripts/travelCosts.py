import travelData
import math
import sys

'''
@params: takes two lat/lon pairs (start and end points)
		 wheelchair = True if passenger is needs accomodations
@returns: the maximum possible taxi cost for a trip with specified 
		  params in dollars 
'''
def taxi(lat1, lon1, lat2, lon2, wheelchair):
	# converts from miles to meters and ceilings to nearest decimal
	miles = math.ceil(travelData.mileage(lat1, lon1, lat2, lon2) / 160.934) / 10

	cost = sys.maxint # so that taxi use is discouraged if this is broken

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

'''
@params: startLat: the pickup point of the first rider
		 startLon: the pickup point of the first rider
		 endLat: the drop off point of the last rider
		 endLon: the drop off point of the last rider
		 uhTravelTime: the amount of time scheduled to handle all trips
		 provider: the provider ID
@returns: the cost of sending a new bus to handle unhandled trip
'''
def newBusRun(startLat, startLon, endLat, endLon, uhTravelTime, provider):
	baselat, baselon = None, None
	costPH = None
	if provider == 6:
		baselat, baselon = 47.530563, -122.322681
		costPH = 51.79
		# print "provider 6"
	elif provider == 5:
		baselat, baselon = 47.591956, -122.182784
		costPH = 46.85
		# print "provider 5"
	else:
		raise ValueError("provider must be 5 or 6")

	preTime = travelData.time(baselat,baselon,startLat,startLon)
	# print preTime
	postTime = travelData.time(endLat,endLon,baselat,baselon)
	# print postTime

	# converts time to hour and raises to hourly ceiling
	totalTime = math.ceil((preTime + uhTravelTime + postTime) / 3600.0)
	# print totalTime

	if totalTime > 4:
		cost = costPH * totalTime
	else:
		cost = costPH * 4
	return cost

# testing purposes
def main():
	print('ambulatory')
	print(taxi(47.602558, -122.142807, 47.631370, -122.142979, False))
	# $ 8.20
	print('wheelchair')
	print(taxi(47.602558, -122.142807, 47.631370, -122.142979, True))
	# $28.00

	print('provider 5')
	print(newBusRun(47.602558, -122.142807, 47.631370, -122.142979, 219, 5))
	# 187.4
	print('provider 6')
	print(newBusRun(47.602558, -122.142807, 47.631370, -122.142979, 219, 6))
	# 207.16

if __name__ == "__main__":
	main()