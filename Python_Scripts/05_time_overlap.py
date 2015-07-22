def time_overlap(Run_Schedule, URID, pickUpDropOff = True):
    '''URID: of class URID, has bookingId, pickUpLocation, dropOffLocation, etc.
        Run_Schedule: Schedule (pd.Data.Frame) of the run on which we're trying to insert the URID
        RETURN: dictionary containing indices of schedule-outbound and -inbound nodes that we need
        to get distance between w/r/t URID location.'''

    #How it works: first, find all nodes that have time overlap with the URID's (pickup or dropoff) window
    # second, notice any gaps in the order of these nodes from the original bus ride.
    # For the first chunk of overlapping nodes, add the lower-time bound node in, given that the first node
    # even exists in the Run_Schedule.
    # For every chunk of contiguous overlap nodes, add in the upper-time bound node, because there can potentially
    # be an inbound ride from the URID node to the upper-time bound node. There can't be an outbound ride.

    if pickUpDropOff:
        Start = URID.PickupStart[0]
        End = URID.PickupEnd[0]
    else:
        Start = URID.DropoffStart[0]
        End = URID.DropoffEnd[0]
        
    crossover = []
    
    for jj in range(Run_Schedule.shape[0]):
        #Checking if a Run's PickupWindow overlaps with URID's Window.
        if Run_Schedule.Activity.iloc[jj] == 0:
            PUE = Run_Schedule.PickupEnd.iloc[jj]; PUS = Run_Schedule.PickupStart.iloc[jj]
            #simple, unequal overlap
            if (PUE > Start) & (PUS < End):
                crossover.append(Run_Schedule.index[jj])
            # equal or strictly within [PUS, PUE]
            if (PUE <= End) & (PUS >= Start):
                crossover.append(Run_Schedule.index[jj])
            # [Start, End] completely covered by [PUS, PUE] and then some on both sides
            if (PUE > End) & (PUS < Start):
                crossover.append(Run_Schedule.index[jj])
            # [Start, End] completely covered and then some only on left side
            if (PUE == End) & (PUS < Start):
                crossover.append(Run_Schedule.index[jj])
            # [Start, End] completely covered and then some only on right side
            if (PUS == Start) & (PUE > End):
                crossover.append(Run_Schedule.index[jj])
                
        #Checking if a Run's DropoffWindow overlaps with URID's Window.
        if Run_Schedule.Activity.iloc[jj] == 1:
            DOE = Run_Schedule.DropoffEnd.iloc[jj]; DOS = Run_Schedule.DropoffStart.iloc[jj]
            if (DOE > Start) & (DOS < End):
                crossover.append(Run_Schedule.index[jj])
            if (DOE <= End) & (DOS >= Start):
                crossover.append(Run_Schedule.index[jj])
            if (DOE > End) & (DOS < Start):
                crossover.append(Run_Schedule.index[jj])
            if (DOE == End) & (DOS < Start):
                crossover.append(Run_Schedule.index[jj])
            if (DOS == Start) & (DOE > End):
                crossover.append(Run_Schedule.index[jj])
                
    #Get rid of cases that repeat themselves:
    crossover = list(set(crossover))
    
    inserts = Run_Schedule.loc[crossover]; inserts = inserts.index
    lst = []; outbound = []; inbound = []
    #Lists of continuously arranged nodes with overlap
    for k, g in groupby(enumerate(inserts), lambda (i,x):i-x):
        k = map(itemgetter(1), g)
        #save nodes with time overlap
        outbound += k; inbound +=k
        #save upper/lower bound where appropriate
        lst += [min(k)]; lst+=[max(k)]
        if len(lst) == 2:
            if lst[0] != min(indices):
                outbound.append(lst[0]-1) #we have a lower bound node, heading outbound from Run_Schedule
            if lst[-1] != max(indices):
                inbound.append(lst[-1]+1) #upper bound node for first contiguous set of overlap nodes
        else:
            if lst[-1] != max(indices):
                inbound.append(lst[-1]+1) #upper bound node for first contiguous set of overlap nodes
    
    outbound, inbound = map(sorted, [outbound, inbound])
    print("Need to service URID within %s sec to %s sec" % (Start, End))
    print("These indices of Run_Schedule will need\nto have distances calculated: %s" % np.union1d(outbound, inbound))

    retDict = {"outbound": outbound, "inbound": inbound, "all_nodes" : sorted(np.union1d(outbound, inbound))}
    return retDict



### TEST THIS FUNCTION ###
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

#data = add_TimeWindows(data_allday, windowsz)
#broken_Run = '680SEB'
#resched_init_time = 800*60 #initial time IN SECONDS that we will begin rerouting buses. Idea is like 2hrs from breakdown time.

#URIDs = get_URIDs(data, broken_Run, resched_init_time)
#testBusData = get_busRuns(data, broken_run)
#urid = URIDS[0]

##formulate inbound nodes and outbound nodes, for input into OSRM!!!
#inserts = time_overlap(Run_Schedule, URID, pickUpDropOff)
#outbound = Run_Schedule.loc[inserts["outbound"]]
#outbound = np.column_stack((np.array(outbound.LAT), np.array(outbound.LON))) #GODDAMNIT THAT WAS COMPLICATED
#inbound = Run_Schedule.loc[inserts["inbound"]]
#inbound = np.column_stack((np.array(inbound.LAT), np.array(inbound.LON))) 
