def time_insertions(Run_Schedule, URID, pickUpDropOff = True):
	'''URID: of class URID, has bookingId, pickUpLocation, dropOffLocation, etc.
		Run_Schedule: Schedule (pd.Data.Frame) of the run on which we're trying to insert the URID

		RETURN: pd.Data.Frame corresponding to nodes with overlapping pickup/dropoff windows'''

	#CURRENT ISSUES: RUNSCHEDULE SHOULD HAVE PRECEDING NODES, AT LEAST ONE PRIOR TO RESCHED_INIT_TIME

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
	crossover = set(crossover)
	print("Need to service URID within %s sec to %s sec" % (Start, End))
	print("These indices of Run_Schedule overlap: %s" % crossover)

return Run_Schedule.loc[crossover]



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

#insertions = time_insertions(testBusData, urid, True)
