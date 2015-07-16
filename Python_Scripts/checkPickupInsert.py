# still need to update all of the ETAs after the insert

import pandas as pd
### Pick the best insertion point and place it in an return a busRun dataframe
### Deals with dwell times somehow. 

import numpy as np

def checkPickupInsert(URID, busRun, distanceTable):
	runs = busRun[busRun.ETA < URID.pickupWindowEnd,['ETA', 'Lat', 'Lon']].index.tolist()
	for run in runs: 







	for i in subset.index.tolist(): 
		times = osrm([URID.latPickup, subset.Lat[i], subset.Lat[i + 1]], [URID.lonPickup, subset.Lon[i], subset.Lon[i + 1]])
		newETA = times[0] + busRun.ETA[i]
		if newETA < URID.pickupWindowEnd:
			if newETA + times[1] < busRun.ETA[i + 1] + 1800:
				newRow = DataFrame({'SchedTime': 'NA', 'ETA' : newETA, 'Lat': URID.latPickup , 
				'Lon': URID.lonPickup, 'BookingId': URID.BookingId, 'SpaceOn': 'later', 'SpaceOff': 'later', 
				'Activity': 0,'MobiAidCode': 'later' }) #need to fix those laters
				toConcat =  [busRun, newRow]
				newBusRun = concat(toConcat)
				newBusRun.sort('ETA', inplace=True)

	
	# row =  getrownum(where busRun$ETA < URID$pickupWindowEnd) # row is a list object
	# time1 = osrm(URID$lat, URID$lon, busRun$lat[row], busRun$lon[row])
	# if(time1 < URID$pickupWindowEnd) 
		# time2 = time1 + osrm(URID$lat, URID$lon, busRun$lat[row+1], busRun$lon[row+1])
		# if time2 < busRun$ETA[row+1] 
			#create a new df with URID inserted at row+1
	
	
	
	
	return(newBusRun)
