












	
	
	
	
		
				'Activity': 0,'MobiAidCode': 'later' }) #need to fix those laters
				'Lon': URID.lonPickup, 'BookingId': URID.BookingId, 'SpaceOn': 'later', 'SpaceOff': 'later', 
				newBusRun = concat(toConcat)
				newBusRun.sort('ETA', inplace=True)
				newRow = DataFrame({'SchedTime': 'NA', 'ETA' : newETA, 'Lat': URID.latPickup , 
				toConcat =  [busRun, newRow]
			#create a new df with URID inserted at row+1
			if newETA + times[1] < busRun.ETA[i + 1] + 1800:
		# if time2 < busRun$ETA[row+1] 
		# time2 = time1 + osrm(URID$lat, URID$lon, busRun$lat[row+1], busRun$lon[row+1])
		if newETA < URID.pickupWindowEnd:
		newETA = times[0] + busRun.ETA[i]
		times = osrm([URID.latPickup, subset.Lat[i], subset.Lat[i + 1]], [URID.lonPickup, subset.Lon[i], subset.Lon[i + 1]])
	# if(time1 < URID$pickupWindowEnd) 
	# row =  getrownum(where busRun$ETA < URID$pickupWindowEnd) # row is a list object
	# time1 = osrm(URID$lat, URID$lon, busRun$lat[row], busRun$lon[row])
	'''
	distances = osrm(URID, subset)
	for i in subset.index.tolist(): 
	for run in runs: 
	return(newBusRun)
	runs = busRun[busRun.ETA < URID.pickupWindowEnd,['ETA', 'Lat', 'Lon']].index.tolist()
	subset = busRun.loc[busRun.ETA < URID.pickupWindowEnd]
# still need to update all of the ETAs after the insert
### Deals with dwell times somehow. 
### Pick the best insertion point and place it in an return a busRun dataframe
'''
def checkPickupInsert(URID, busRun):
import numpy as np
import pandas as pdss