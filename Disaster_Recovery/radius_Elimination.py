from time_overlap import time_overlap

#print distances that bus 181SEB is from URID location during time windows... It's pretty far...
def radius_Elimination(data, URID, radius):
    '''Given a set of the day's bus data and an unhandled requst,
    eliminate all bus routes that are farther than radius-miles away at all
        points in the URID's pickup window. Run time_insertions.py on the resultant list.

        NOTE: you need to "> pip install haversine"

        INPUT:  data - pd.Data.Frame returned from add_TimeWindows.py
                URID - URID object from get_URIDS.py    
                radius - float, number of miles
                pickUpDropOff - boolean True/False for PickUp (True) or Dropoff (False)

        RETURN: LIST of runs within radius-miles of URID.'''

    #first, resolve indexing issues if index column is type timedate
    if type(data.index[0]) != int:
        data.index = range(0, data.shape[0])

    #obviously, broken bus can't be in the list of nearby buses.
    data_copy = data[data.Run != URID.Run]

    URID_loc = ([URID.PickUpCoords[0], URID.PickUpCoords[1]])
        
    #get pd.Data.Frame of nodes that have overlap with URID's pickup or dropoff window
    overlap_data = time_overlap(data_copy, URID)

    #get row index of nodes that may have either inbound/outbound overlap with URID TW.
    overlap_data = data.loc[overlap_data['all_nodes']]
    overlap_LAT = overlap_data.LAT.tolist()
    overlap_LON = overlap_data.LON.tolist()

    #store list of rides that are sufficiently nearby URID's location
    okBuses = []
    for k in range(len(overlap_LAT)):
        point = (overlap_LAT[k], overlap_LON[k])
        dist = haversine.haversine(point, URID_loc, miles=True)
        if(dist < radius):
            okBuses.append(overlap_data.Run.iloc[k])

    ret = list(set(okBuses))
    if len(ret) > 30:
        radius -= 1
        ret = radius_Elimination(data, URID, radius)

    return ret



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






