import travelData
import math
import sys

'''
@params: takes two lat/lon pairs (start and end points)
		 wheelchair = True if passenger is needs accomodations
@returns: the maximum possible taxi cost for a trip with specified 
		  params in dollars 
'''

def wheelchair_present(URID):
	#check if URID has a wheelchair, returns Boolean True/False:

	mobaids = URID.SpaceOn.tolist()[0]
	WC = False
	if type(mobaids) == str:
        WC = any(['W' in x for x in mobaids.split(',')])
    return WC


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
@params: busRun: a clean busRun starting with activity code 0 and ending with 1
		 provider: the provider ID. That is, busRun should be abbreviated to begin
		 at the first URID.
@returns: the cost of sending a new bus to handle unhandled trip
'''
def newBusRun_cost(busRun, provider):
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

	# start and end of bus run
	firstRow = busRun.iloc[0]
	lastRow = busRun.iloc[busRun.shape[0] - 1]

	# get coords and total active trip time
	startLat = firstRow['LAT']
	startLon = firstRow['LON']
	endLat = lastRow['LAT']
	endLon = lastRow['LON']
	uhTravelTime = lastRow['DropoffEnd'] - firstRow['PickupStart']

	preTime = travelData.time(baselat,baselon,startLat,startLon)
	# print preTime
	postTime = travelData.time(endLat,endLon,baselat,baselon)
	# print postTime

	# converts time to hour and raises to hourly ceiling
	totalTime = math.ceil((preTime + uhTravelTime + postTime) / 3600.0)
	# print totalTime

	# busses have to run for at least 4 hours
	if totalTime > 4:
		cost = costPH * totalTime
	else:
		cost = costPH * 4
	return cost

# testing purposes
def main():
	from get_busRuns import get_busRuns
	from get_URIDs import get_URIDs
	import pandas as pd

	print('2mi ambulatory taxi')
	print('cost: $' + str(taxi(47.602558, -122.142807, 47.631370, -122.142979, False)))
	# $ 8.20
	print('2mi wheelchair taxi')
	print('cost: $' + str(taxi(47.602558, -122.142807, 47.631370, -122.142979, True)))
	# $28.00

	data = pd.read_csv('../data/single_day_TimeWindows.csv')
	bus = '680SEB'
	print('Run 680SEB after 15:21 4/14/14 on provider 5')
	print('cost: $' + str(newBusRun(get_busRuns(data , bus, get_URIDs(data, bus, 53684)[1]), 5)))
	# 187.4
	print('Run 680SEB after 15:21 4/14/14 on provider 6')
	print('cost: $' + str(newBusRun(get_busRuns(data , bus, get_URIDs(data, bus, 53684)[1]), 6)))
	# 207.16

if __name__ == "__main__":
	main()