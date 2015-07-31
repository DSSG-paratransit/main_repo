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

	pickup_inserts = time_overlap(Run_Schedule, URID, pickUpDropOff = True)
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
	print(newETA < bound)
	leftover = bound - newETA
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
	dropoff_inserts = time_overlap(Run_Schedule_Lag, URID, pickUpDropOff = False)
	dropoff_all_nodes = filter(lambda x: x >= comeback1, dropoff_inserts["all_nodes"])
	dropoff_outbound = filter(lambda x: x >= comeback1, dropoff_inserts["outbound"])
	# can't return to first outbound node:
	dropoff_inbound = filter(lambda x: x > comeback1, dropoff_inserts["inbound"])
	if dropoff_outbound[0] == dropoff_inbound[0]: dropoff_inbound.pop(0)

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
	           "total_lag" : total_lag, 'RunID' : Run_Schedule.Run.iloc[0]}



def originalLateness(Run_Schedule):
    '''
    Run_Schedule: Pandas dataframe containing Trapeze-scheduled bus route and time windows, Run is listed in good_buses
    URID: of class URID

    return: pandas dataframe with 2 columns: 'break_TW' (binary variable
        indicating whether future stop will be late), 'late' (integer indicating how late bus will be to stop).
    '''

    lateness_score = np.zeros((Run_Schedule.shape[0],2))
    row_ctr = 0
    #Don't count lateness when the bus is leaving garage.
    for k in range(Run_Schedule.index.min(),(Run_Schedule.index.max()+1)):
        if (Run_Schedule.Activity.loc[k] not in [0,1]):
            row_ctr += 1
        else:
            bound = max(Run_Schedule.PickupEnd.loc[k], Run_Schedule.DropoffEnd.loc[k])
            eta = Run_Schedule.ETA.loc[k]
            #0 indicates TW not broken, 1 otherwise.
            lateness_score[row_ctr, 0] = int(eta > bound)
            #if time window is broken, by how much?
            lateness_score[row_ctr, 1] = max(0, eta - bound)
            #print(dropoff_score[row_ctr,:])
            row_ctr+=1

    ret = pd.DataFrame({"break_TW": lateness_score[:,0], "late": lateness_score[:,1]})

    return ret






	