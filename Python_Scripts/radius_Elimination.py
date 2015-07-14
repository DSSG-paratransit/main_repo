def radius_Elimination(data, URID, radius, pickUpDropOff):
	'''Given a set of the day's bus data and an unhandled requst,
		eliminate all bus routes that are farther than radius-miles away at all
		points in the URID's pickup or dropoff window, the window being specified
		by pickUpDropOff. Run time_insertions.py on the resultant list.

		NOTE: you need to "> pip install haversine"

		INPUT:  data - pd.Data.Frame returned from add_TimeWindows.py
				URID - URID object from get_URIDS.py	
				radius - float, number of miles
				pickUpDropOff - boolean True/False for PickUp (True) or Dropoff (False)

		RETURN: LIST of runs within radius-miles of URID.'''

	import haversine from haversine

	#obviously, broken bus can't be in the list of nearby buses.
	data = data[data.Run != URID.Run]

	#get pd.Data.Frame of nodes that have overlap with URID's pickup or dropoff window
	overlap_data = time_insertions(data, URID, pickUpDropOff)

	if pickUpDropOff:
		URID_loc = ([URID.PickUpCoords["LAT"], URID.PickUpCoords["LON"]])
	else:
		URID_loc = ([URID.DropOffCoords["LAT"], URID.PickUpCoords["LON"]])

	overlap_LAT = overlap_data.LAT.tolist()
	overlap_LON = overlap_data.LON.tolist()

	#store list of rides that are sufficiently nearby URID's location
	okBuses = []
	for k in range(len(overlap_LAT)):
    	point = (overlap_LAT[k], overlap_LON[k])
    	dist = haversine(point, URID_loc, miles=True)
    	if(dist < radius):
    		okBuses.append(overlap_data.Run.iloc[k])

    okBuses = set(okBuses)



### TEST THIS FUNCTION ###

#import pandas as pd
#import numpy as np
#from haversine import haversine

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds
#newdata = add_TimeWindows(data_allday, windowsz)

#broken_Run = data.Run.unique()[0]
#resched_init_time = 14*60*60
#urids = get_URIDs(newdata, broken_Run, resched_init_time) 	

#URID = urids[0]
#radius = 20 #miles
#checkBuses = radius_Elimination(newdata, URID, radius, True)






