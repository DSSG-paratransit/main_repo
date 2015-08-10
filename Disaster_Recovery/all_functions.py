import pandas as pd
import numpy as np
import haversine
import operator
import math
import os
import requests
import sys
import re
import time
import read_fwf
import itertools
import operator
# import add_TimeWindowsCapacity as aTWC
import checkCapacityInsertPts as checkCap
from boto.s3.connection import S3Connection


def s3_data_acquire(AWS_ACCESS_KEY, AWS_SECRET_KEY, path_to_data, qc_file_name = 'qc_streaming.csv'):
    '''
    Args:
    AWS_ACCESS_KEY (str): aws access key
    AWS_SECRET_KEY (str): aws secret key
    path_to_data (str): where should S3 data be stored to, locally?
    qc_file_name (str): what should the qc'ed S3 file be called?

    Returns:
    QC'ed day's schedule (pd.read_csv(read_me))

    '''

    os.chdir(path_to_data)

    #For establishing connection, use access and secret keys sent by Valentina.

    #STEP 1: Access S3 and download relevant streaming data file
    from boto.s3.connection import S3Connection
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    conn.get_all_buckets()

    bucket = conn.get_bucket('paratransitdata')

    #print bucket contents:
    rs = bucket.list()

    #get list of streaming_data files for today's date
    file_ls = []
    for key in rs:
        if re.search("streaming_data/Schedules_"+ time.strftime('%Y%m%d'),key.name.encode('ascii')):
            file_ls.append(key.name.encode('ascii'))

    #select relevant streaming_data file:
    data_key = bucket.get_key(file_ls[-1])
    move_to_me = 'real_time_data.csv'
    data_key.get_contents_to_filename(move_to_me)


    #STEP 2: change this file from fixed width formatted to tab delimitted
    # NOTE: datatypes are screwed up.
    data = read_fwf.read('real_time_data.csv')

    #STEP 3: QC this file a la the R QCing script
    data56 = data.loc[(data.ProviderId == '5') | (data.ProviderId == '6')]
    rides = data56.Run.unique()
    data56.loc[:,'Activity'] = data56.loc[:,'Activity'].astype('int')

    #lat/lon constraints:
    upper_right = [49.020430, -116.998768]
    lower_left = [45.606961, -124.974842]
    minlat = lower_left[0]; maxlat = upper_right[0]
    minlon = lower_left[1]; maxlon = upper_right[1]


    #Write the cleaned up data:
    ctr = 0
    for ride in rides:
        temp_ride = data56.loc[data56.Run == ride]
        temp_ride.drop(temp_ride.columns[0], axis = 1)
        
        flag = 1 #1 == good, 0 == eliminate.
        lats = temp_ride.LAT; lons = temp_ride.LON
        #eliminate runs from roster that have bad lat/lon data:
        if(any(lats < minlat) | any(lats>maxlat) | any(lons<minlon) | any(lons > maxlon)):
            flag = 0
        #eliminate runs that don't move
        if(all(lats == lats.iloc[0]) | all(lons == lons.iloc[0])):
            flag = 0
        #eliminate runs that don't leave a garage and return to a garage
        if (temp_ride.Activity.iloc[0] != 4.) | (temp_ride.Activity.iloc[-1] != 3.):
            flag = 0
            
        temp_ride = temp_ride.drop(temp_ride.columns[0], axis = 1)
        
        if (ctr == 0) & (flag == 1):
            temp_ride.to_csv(qc_file_name, mode = 'a', header = True, index = False)
            ctr +=1
        if (ctr != 0) & (flag == 1) :
            temp_ride.to_csv(qc_file_name, mode = 'a', header = False, index = False)

    read_me = path_to_data+qc_file_name

    return pd.read_csv(read_me)

'''
@params: takes a string containing 24h time in HH:MM format 
@returns: the passed in value converted to seconds
'''
def humanToSeconds(hhmm):

    # Invalid format
    format = re.compile('\d\d:\d\d')
    if(format.match(hhmm) is None):
        raise ValueError('Time provided is in incorrect format')
    
    hoursAndSeconds = re.findall('\d\d', hhmm)


    hour = int(hoursAndSeconds[0])
    sec = int(hoursAndSeconds[1])

    # Invalid Time
    if(hour > 24 or sec > 59):
        raise ValueError('Time provided is invalid')

    return(hour * 3600 + sec * 60)


def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA.
        data is subsetted schedule data from a day.
        windowsz is size of pickup/dropoff window in seconds'''

    etas = data.ix[:,"ETA"]
    schtime =data.ix[:,"SchTime"]
    Activity = data.ix[:, "Activity"]
    ReqLate = data.ix[:, "ReqLate"]

    schtime_arr = np.array(schtime.tolist())
    nrow = data.shape[0]
    PickupStart = np.zeros(nrow); PickupEnd = np.zeros(nrow)
    DropoffStart = np.zeros(nrow); DropoffEnd = np.zeros(nrow)

    for x in range(0, nrow):

    #make dropoff window when there's no required drop off time
        if (Activity[x] == 1) & (ReqLate[x] <0):
            DropoffStart[x] = etas[x]-3600
            DropoffEnd[x] = etas[x]+3600

        #make dropoff window when there IS a required drop off time: 1hr before ReqLate time
        if (Activity[x] == 1) & (ReqLate[x] >0):
            DropoffStart[x] = etas[x]-3600
            DropoffEnd[x] = ReqLate[x]  

        #schtime is in the middle of the pick up window
        if Activity[x] == 0:
            PickupStart[x] = schtime[x]-(windowsz/2)
            PickupEnd[x] = schtime[x]+(windowsz/2)
        
    data.insert(len(data.columns), 'PickupStart',  pd.Series((PickupStart), index=data.index))
    data.insert(len(data.columns), 'PickupEnd',  pd.Series((PickupEnd), index=data.index))
    data.insert(len(data.columns), 'DropoffStart',  pd.Series(DropoffStart, index=data.index))
    data.insert(len(data.columns), 'DropoffEnd',  pd.Series(DropoffEnd, index=data.index))

    return data.copy()

class URID:
    def __init__(self, BookingId, Run, PickUpCoords, DropOffCoords, PickupStart, PickupEnd, DropoffStart, DropoffEnd, SpaceOn, MobAids, wcOn, wcOff, amOn, amOff, PickupInsert, DropoffInsert):
        self.BookingId= BookingId
        self.Run = Run
        self.PickUpCoords = PickUpCoords
        self.DropOffCoords = DropOffCoords
        self.PickupStart = PickupStart
        self.PickupEnd = PickupEnd
        self.DropoffStart = DropoffStart
        self.DropoffEnd = DropoffEnd
        self.SpaceOn = SpaceOn
        self.MobAids = MobAids
        self.wcOn = wcOn
        self.wcOff = wcOff
        self.amOn = amOn
        self.amOff = amOff
        self.PickupInsert = PickupInsert
        self.DropoffInsert = DropoffInsert 


def get_URID_Bus(data, broken_Run, resched_init_time, add_stranded = False, BREAKDOWN_LOC = None):
    '''get unscheduled request id's from broken bus,
        based on when we're allowed to first start rescheduling.
        resched_init_time is in seconds, marks the point in time we can begin considering reinserting new requests.
        broken_Run is number of run that breaks
        data is today's scheduling data

        RETURN: list of URIDs'''
    
    #all rides that exist past time we're allowed to begin rescheduling
    leftover = data[data["ETA"] >= resched_init_time]
    leftover = leftover[(leftover["Activity"] != 6) & (leftover["Activity"] != 16) & (leftover["Activity"] != 3)]
    
    #rides that were scheduled to be on broken bus past resched_init_time
    unsched = leftover[leftover["Run"]==broken_Run]
    diffIDs = unsched.BookingId.unique()
    diffIDs = diffIDs[~np.isnan(diffIDs)]

    print("There are %s rides left to be scheduled on broken run %s" % (unsched.shape[0], broken_Run))

    saveme = []

    #save separate URID's in a list
    for ID in diffIDs:
        my_info = unsched[unsched["BookingId"]==ID]
        #if person is already on bus when breakdown occurs,
        #need to handle URID differently:
        if(my_info.shape[0] == 1 & add_stranded):
            temp = URID(BookingId = ID,
                Run = broken_Run,
                #if person is stranded on bus, their PickUpCoords are the BREAKDOWN_LOC (global var)
                PickUpCoords = pd.Series(data = np.array(BREAKDOWN_LOC), index = ["LAT", "LON"]),
                DropOffCoords = my_info[["LAT", "LON"]].ix[0,],
                PickupStart = resched_init_time,
                PickupEnd = resched_init_time+30*60,
                DropoffStart = int(my_info[["DropoffStart"]].ix[0,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].ix[0,]),
                SpaceOn = my_info[["SpaceOn"]].ix[0,],
                MobAids = my_info[["MobAids"]].ix[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,],
                PickupInsert = 0,
                DropoffInsert = 0)
            saveme.append(temp)
        if(my_info.shape[0] != 1):
            temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = my_info[["LAT", "LON"]].ix[0,],
                DropOffCoords = my_info[["LAT", "LON"]].ix[1,],
                PickupStart = int(my_info[["PickupStart"]].ix[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].ix[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].ix[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].ix[1,]),
                SpaceOn = my_info[["SpaceOn"]].ix[0,],
                MobAids = my_info[["MobAids"]].ix[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,],
                PickupInsert = 0,
                DropoffInsert = 0)
            saveme.append(temp)

    return saveme


def get_URID_BookingIds(data, BookingId_list):
    '''get unscheduled request id's from broken bus,
    based on the list of BookingIds provided by dispatcher

    RETURN: list of URIDs'''

    diffIDs = BookingId_list
    saveme = []
    for ID in diffIDs:
        my_info = data[data["BookingId"]==ID]
        temp = URID(BookingId = ID,
                Run = my_info['Run'].ix[0,],
                PickUpCoords = my_info[["LAT", "LON"]].iloc[0,],
                DropOffCoords = my_info[["LAT", "LON"]].iloc[1,],
                PickupStart = int(my_info[["PickupStart"]].iloc[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].iloc[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].iloc[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].iloc[1,]),
                SpaceOn = my_info[["SpaceOn"]].iloc[0,],
                MobAids = my_info[["MobAids"]].iloc[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,],
                PickupInsert = 0,
                DropoffInsert = 0)
        
        saveme.append(temp)

    #return sorted URIDs based on PickupStart time
    return sorted(saveme, key = operator.attrgetter('PickupStart'))


def time_overlap(Run_Schedule, URID, pudo = True):
    '''
    Args:

    Run_Schedule (pd.DataFrame): pd.DataFrame containing any number of bus runs. Must have time window columns.

    URID (class.object): of class URID

    pudo (boolean): 'pickupdropoff', check pickup windows or drop off windows?

    Returns: 

    retDict (dict): dictionary containing indices of schedule-outbound and -inbound nodes that we need
        to get distance between w/r/t URID location.'''

    #How it works: first, find all nodes that have time overlap with the URID's (pickup or dropoff) window
    # second, notice any gaps in the order of these nodes from the original bus ride.
    # For the first chunk of overlapping nodes, add the lower-time bound node in, given that the first node
    # even exists in the Run_Schedule.
    # For every chunk of contiguous overlap nodes, add in the upper-time bound node, because there can potentially
    # be an inbound ride from the URID node to the upper-time bound node. There can't be an outbound ride.

    if pudo:
        Start = URID.PickupStart
        End = URID.PickupEnd
    else:
        Start = URID.DropoffStart
        End = URID.DropoffEnd
        
    crossover = []
    
    for jj in range(Run_Schedule.shape[0]):
        #Checking if a Run's PickupWindow overlaps with URID's Window.
        WinSt = max(Run_Schedule.PickupStart.iloc[jj], Run_Schedule.DropoffStart.iloc[jj])
        WinEnd = max(Run_Schedule.PickupEnd.iloc[jj], Run_Schedule.DropoffEnd.iloc[jj])

        #simple, unequal overlap
        if (WinEnd > Start) & (WinSt < End):
            crossover.append(Run_Schedule.index[jj])
        # equal or strictly within [WinSt, WinEnd]
        if (WinEnd <= End) & (WinSt >= Start):
            crossover.append(Run_Schedule.index[jj])
        # [Start, End] completely covered by [WinSt, WinEnd] and then some on both sides
        if (WinEnd > End) & (WinSt < Start):
            crossover.append(Run_Schedule.index[jj])
        # [Start, End] completely covered and then some only on left side
        if (WinEnd == End) & (WinSt < Start):
            crossover.append(Run_Schedule.index[jj])
        # [Start, End] completely covered and then some only on right side
        if (WinEnd > End) & (WinSt == Start):
            crossover.append(Run_Schedule.index[jj])
                
    #Get rid of cases that repeat themselves:
    crossover = list(set(crossover))
    
    inserts = Run_Schedule.loc[crossover]; indices = Run_Schedule.index
    lst = []; outbound = []; inbound = []
    #Lists of continuously arranged nodes with overlap
    for k, g in itertools.groupby(enumerate(inserts.index), lambda (i,x):i-x):
        k = map(operator.itemgetter(1), g)
        #save upper/lower bound where appropriate
        lst += [min(k)]; lst+=[max(k)]
        if len(lst) == 2:
            outbound += k; inbound +=k
            if Run_Schedule.Activity.loc[lst[0]] != 4:
                outbound.append(lst[0]-1) #we have a lower bound node, heading outbound from Run_Schedule
            else:
                inbound.pop(0) #if first node is leave garage, can't add lower bound,
                               #and therefore can't return from having left from lower bound
        else:
            outbound += k
            inbound +=k[1:len(k)]
        
        inbound.append(lst[-1]+1) #upper bound node for each contiguous set of overlap nodes
    
    outbound, inbound = map(sorted, [outbound, inbound])
    all_nodes = sorted(np.union1d(outbound, inbound))
    #print("These indices of Run_Schedule will need to have distances calculated:\n%s" % np.union1d(outbound, inbound))

    retDict = {"outbound": outbound, "inbound": inbound, "all_nodes" : all_nodes}
    return retDict


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

    URID_loc = ([URID.PickUpCoords["LAT"], URID.PickUpCoords["LON"]])
        
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

    return list(set(okBuses))


def get_busRuns(data, Run, URID):
      '''
      data (pd.DataFrame): output from add_Time_Windows.py
      Run (str): Run number
      URID (class.URID): URID class object
      resched_init_time (int): number of seconds in day we allow first rescheduling
      RETURN: busRun pandas.dataframe for specified Run.'''

      # leave garage (beginning of route index), gas (end of route index)
      # get all rides between/including leave garage and gas indices.
      dataSub = data[(data["Run"] == Run)]# & (data['ETA'] >= resched_init_time)]

      # if full busRun or partial
      if URID is None:
            #subset only the rides that aren't 6, 16, or 3:
            leaveIndex = dataSub.index.min()
      else:
            leave = dataSub[(dataSub['LAT'] == URID.PickUpCoords.LAT) 
                  & (dataSub['LON'] == URID.PickUpCoords.LON) 
                  & (dataSub['BookingId'] == URID.BookingId)]
            leaveIndex = leave.index.min()

      baseIndex = dataSub[(dataSub["Activity"]==6)|(dataSub["Activity"]==16)|(dataSub["Activity"]==3)].index.min()
      busRun = data.iloc[leaveIndex:baseIndex+1]

      return busRun


def osrm (URID_location, inbound, outbound):
    #URID_location it's a list: [lat, lon]
    #lists for inbound and outbound matrices
    # inbound/outbound: 2-column np.arrays storing inbound/outbound node latitude/longitude
    # and inbound (from scheduled location to urid location) 
    total_times = []
    out_start_points = []
    out_end_points = []
    in_total_time = []
    in_start_points = []
    in_end_points = []
    osrm_url = "http://router.project-osrm.org/viaroute?"
    urid_LAT = URID_location[0]; urid_LON = URID_location[1]

    # outbound
    for k in range(outbound.shape[0]): 
        lat_cord_O = outbound[k, 0]; lon_cord_O = outbound[k, 1]
        lat_cord_I = inbound[k, 0]; lon_cord_I = inbound[k, 1]
        
        route_url = osrm_url+ "loc=" + str(lat_cord_O) + "," + str(lon_cord_O) + "&loc=" + str(urid_LAT) + "," + str(urid_LON) + "&loc=" + str(lat_cord_I) + "," + str(lon_cord_I) +"&instructions=false"
        route_requests = requests.get(route_url)
        route_results = route_requests.json()
        if not route_results:
            print("FOUND NO ROUTE FROM INDEX {0}".format((outbound[k,0], outbound[k,1])))
            quit()
        total_times += [route_results[u'route_summary'][u'total_time']]

    a = np.array([total_times])
    
    return(a.T)


def insertFeasibility(Run_Schedule, URID):

    '''
    Run_Schedule: Pandas dataframe containing Trapeze-scheduled bus route and time windows, Run is listed in good_buses
    URID: of class URID

    return: dictionary. Largest component of dictionary is 'score,' a pd.df with 'break_TW' (binary variable
        indicating whether future stop will be late), 'late' (integer indicating how late bus will be to stop),
        and 'node' (the index, of the node within the Run_Schedule)
        Also return 'total_lag', the total number of seconds by which the bus is currently late.
        Also return 'pickup_insert' and 'dropoff_insert', i.e. indices of the best insertion point of URID on to Run_Schedule.
    '''

    # FEASIBILITY OF PICK UP:

    #location from where we'll pick up given URID.
    uridLoc = [URID.PickUpCoords[0], URID.PickUpCoords[1]]

    pickup_inserts = time_overlap(Run_Schedule, URID)
    outbound = Run_Schedule.loc[pickup_inserts["outbound"]]
    outbound = np.column_stack((np.array(outbound.LAT), np.array(outbound.LON)))
    inbound = Run_Schedule.loc[pickup_inserts["inbound"]]
    inbound = np.column_stack((np.array(inbound.LAT), np.array(inbound.LON)))

    time_matrix_pickup = osrm(uridLoc, inbound, outbound)

    #start picking best pickup insertion:
    rt_times = sorted(enumerate(time_matrix_pickup), key=operator.itemgetter(1)) #use itemgetter(1) because (0) is index from enumerator!

    #smallest round trip travel time, corresponding rows on bus's schedule:
    best_rt_time = rt_times[0][1]
    #row indices on Run_Schedule between which to insert:
    leave1 = pickup_inserts["outbound"][rt_times[0][0]] #leave this scheduled node
    comeback1 = pickup_inserts["inbound"][rt_times[0][0]] #come back to this scheduled node

    dwell = 500

    #get total lag time, see if next time window is broken:
    newETA = Run_Schedule.ETA.loc[leave1] + dwell + best_rt_time
    bound = max(Run_Schedule.PickupEnd.loc[comeback1], Run_Schedule.DropoffEnd.loc[comeback1])

    #is the next time window broken?
    lag1 = newETA - Run_Schedule.ETA.loc[comeback1]

    #count number of broken time windows for rest of trip:
    #to be able to count broken windows, amt by which they're broken,
    #insert_score will contain (0) TW broken yes/no; (1) amount by which window broken
    pickup_score = np.zeros(((Run_Schedule.index.max() - comeback1 + 1),2)) 
    row_ctr = 0
    for k in range(comeback1,(Run_Schedule.index.max()+1)):
        if (Run_Schedule.Activity.loc[k] not in [0,1]):
            row_ctr += 1
        else:
            bound = max(Run_Schedule.PickupEnd.loc[k], Run_Schedule.DropoffEnd.loc[k])
            eta_future = Run_Schedule.ETA.loc[k] + lag1
            #0 indicates TW not broken, 1 otherwise.
            pickup_score[row_ctr, 0] = int(eta_future > bound)
            #if time window is broken, by how much?
            pickup_score[row_ctr, 1] = max(0, eta_future - bound)
            #print(pickup_score[row_ctr,:])
            row_ctr+=1

    #FEASIBILITY OF DROPOFF:
    Run_Schedule_Lag = Run_Schedule.copy()
    ETAlag = Run_Schedule.ETA + lag1
    Run_Schedule_Lag.ETA = ETAlag
    dropoff_inserts = time_overlap(Run_Schedule_Lag, URID, pudo = False)
    dropoff_all_nodes = filter(lambda x: x >= comeback1, dropoff_inserts["all_nodes"])
    dropoff_outbound = filter(lambda x: x >= comeback1, dropoff_inserts["outbound"])
    # can't return to first outbound node:
    dropoff_inbound = filter(lambda x: x > comeback1, dropoff_inserts["inbound"])

    #corner cases: we pick up and there's no way to drop off before activity code 16:
    if (not dropoff_inbound) | (not dropoff_inbound):
        return {}

    if dropoff_outbound[0] == dropoff_inbound[0]:
        print('First outbound and first inbound for drop off are the same.')
        dropoff_inbound.pop(0)

    outbound = Run_Schedule_Lag.loc[dropoff_outbound]
    outbound = np.column_stack((np.array(outbound.LAT), np.array(outbound.LON)))
    inbound = Run_Schedule_Lag.loc[dropoff_inbound]

    inbound = np.column_stack((np.array(inbound.LAT), np.array(inbound.LON)))

    uridLoc = [URID.DropOffCoords[0], URID.DropOffCoords[1]]
    #second iteration of distance matrix, for drop off routing:
    time_matrix_dropoff = osrm(uridLoc, inbound, outbound)

    #start picking best pickup insertion:
    rt_times = sorted(enumerate(np.sum(time_matrix_dropoff, 1)), key=operator.itemgetter(1)) #use itemgetter(1) because (0) is index from enumerator!

    #smallest round trip travel time, corresponding rows on bus's schedule:
    best_rt_time = rt_times[0][1]
    #rows on Run_Schedule between which to insert:
    leave2 = dropoff_outbound[rt_times[0][0]] #leave this scheduled node
    comeback2 = dropoff_inbound[rt_times[0][0]] #come back to this scheduled node

    #get total lag time, see if next time window is broken:
    newETA = Run_Schedule_Lag.ETA.loc[leave2] + dwell + best_rt_time
    bound = max(Run_Schedule_Lag.PickupEnd.loc[comeback2], Run_Schedule_Lag.DropoffEnd.loc[comeback2])
    #total lag: lag from pickup, and then difference between lagged eta and eta for coming back from pickup
    total_lag = newETA - Run_Schedule_Lag.ETA.loc[comeback2] + lag1

    #count number of broken time windows from dropping off URID:
    dropoff_score = np.zeros(((Run_Schedule_Lag.index.max() - comeback2 + 1),2)) 
    row_ctr = 0
    for k in range(comeback2,(Run_Schedule_Lag.index.max()+1)):
        if (Run_Schedule.Activity.loc[k] not in [0,1]):
            row_ctr += 1
        else:
            bound = max(Run_Schedule_Lag.PickupEnd.loc[k], Run_Schedule_Lag.DropoffEnd.loc[k])
            eta_future = Run_Schedule_Lag.ETA.loc[k] + total_lag
            #0 indicates TW not broken, 1 otherwise.
            dropoff_score[row_ctr, 0] = int(eta_future > bound)
            #if time window is broken, by how much?
            dropoff_score[row_ctr, 1] = max(0, eta_future - bound)
            #print(dropoff_score[row_ctr,:])
            row_ctr+=1

    #assemble output:
    pickup_df = pd.DataFrame({"nodes": range(comeback1,Run_Schedule.index.max()+1), "break_TW": pickup_score[:,0], "late": pickup_score[:,1]})
    dropoff_df = pd.DataFrame({"nodes": range(comeback2,Run_Schedule.index.max()+1), "break_TW": dropoff_score[:,0], "late": dropoff_score[:,1]})
    test = pickup_df[(pickup_df['nodes'] >= comeback1) & (pickup_df['nodes'] < comeback2)]
    ret = {"score": test.append(dropoff_df), "pickup_insert":(leave1, comeback1), "dropoff_insert":(leave2, comeback2),
               "total_lag" : total_lag, 'RunID' : Run_Schedule.Run.iloc[0], 'URID_pickup_ETA': }

    return(ret)


def wheelchair_present(URID):
    #check if URID has a wheelchair, returns Boolean True/False:

    mobaids = URID.SpaceOn.tolist()[0]
    WC = False
    if type(mobaids) == str:
        WC = any(['W' in x for x in mobaids.split(',')])
    return WC

def mileage (lat1, lon1, lat2, lon2):
    '''@params: takes two lat/lon pairs (start and end points)
    @returns: the total street network distance between the pairs
    '''
    route_results = getOSRMOutput(lat1, lon1, lat2, lon2)
    total_dist = route_results[u'route_summary'][u'total_distance']
    #print total_dist
    return(total_dist)


def travel_time (lat1, lon1, lat2, lon2):
    '''
    @params: takes two lat/lon pairs (start and end points)
    @returns: the total non traffic time it would take to get between the two pairs
    '''
    route_results = getOSRMOutput(lat1, lon1, lat2, lon2)
    total_time = route_results[u'route_summary'][u'total_time']
    # print total_time
    return(total_time)


def getOSRMOutput (lat1, lon1, lat2, lon2):
    '''
    @params: takes two lat/lon pairs (start and end points)
    @returns: a json object containing data about traveling between the two pairs
    '''
    osrm_url = "http://router.project-osrm.org/viaroute?"
    route_url = osrm_url+ "loc=" + str(lat1) + "," + str(lon1)
    route_url = route_url + "&loc=" + str(lat2) + "," + str(lon2) + "&instructions=false"
    #print route_url
    route_requests = requests.get(route_url)
    route_results = route_requests.json()
    #print route_results
    return route_results


def taxi(lat1, lon1, lat2, lon2, wheelchair):
    # converts from miles to meters and ceilings to nearest decimal
    miles = math.ceil(mileage(lat1, lon1, lat2, lon2) / 160.934) / 10

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


def write_insert_data(URID, list_Feasibility_output, path_to_output, taxi_cost):
    '''
        Args:

        list_Feasibility_output (list of dicts): some of the top insertion options from busRescheduler loop that are assembled
        into a list (like 'ordered_inserts' in busRescheduler)

        taxi_cost (double): cost of sending URID to taxi

        Return:
        None

        Write:
        {BookingID}_insert_data.txt containing lag, number of late windows, average lateness'''

    if not os.path.isdir(path_to_output):
        os.mkdir(path_to_output)

    file_name = path_to_output + '/' + str(int(URID.BookingId)) + '_insert_data.txt'
    text_file = open(file_name, "w")
    ctr = 1;
    for option in list_Feasibility_output:
        number_late = sum(option['score']['break_TW'].tolist())
        avg_late = sum(option['score']['late'].tolist())/number_late

        text_file.write('OPTION {0}:\n'.format(ctr))
        text_file.write('Put {0} onto bus {1} \n'.format(int(URID.BookingId), option['RunID']) )
        text_file.write('Total lag: {0} \n'.format(int(option['total_lag'])))
        text_file.write('Number of exceeded time windows: {0} \n'.format(number_late))
        text_file.write('Average lateness: {0} \n\n\n'.format(avg_late))
        ctr+=1

    text_file.write('Taxi cost: {0}'.format(taxi_cost))
    text_file.close()
    return None


def day_schedule_Update(data, top_Feasibility, URID):
    '''
    Args:
    data (pd.DataFrame): current schedule for all day's operations

    top_Feasibility (dict): insertion of URID on to bus resulting in min. lag.
        should be [0] element of ordered_inserts

    Returns:
    return (pd.DataFrame): updated (re-arranged) schedule URID properly
        put on to new bus from old bus'''

    tmp = data.copy()
    my_rows = data[data['BookingId']==URID.BookingId]
    #make sure we change the RunID of the URID when placed on new bus!
    tmp.ix[my_rows.index[:], 'Run'] = top_Feasibility['RunID']

    old_pickup_index = my_rows.index[0]
    old_dropoff_index = my_rows.index[1]
    new_pickup_index = top_Feasibility['pickup_insert'][1]
    new_dropoff_index = top_Feasibility['dropoff_insert'][1]

    ind = tmp.index.tolist()
    ind.pop(old_pickup_index)
    ind.pop(old_dropoff_index-1)
    ind.insert(ind.index(new_pickup_index), old_pickup_index)
    ind.insert(ind.index(new_dropoff_index), old_dropoff_index)
    
    return tmp.reindex(ind)


def newBusRun_cost(busRun, provider):
    '''
    Args:
    busRun (pd.DataFrame): pandas df with some bus's whole schedule

    provider (int): provider code of bus contractor (5 or 6)

    Returns:
    cost (float): cost of sending a new bus out to service all URIDs
    '''
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

    preTime = travel_time(baselat,baselon,startLat,startLon)
    # print preTime
    postTime = travel_time(endLat,endLon,baselat,baselon)
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




