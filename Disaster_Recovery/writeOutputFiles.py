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

    file_name = os.path.join(path_to_output, str(str(int(URID.BookingId))+'_insert_data.txt'))
    text_file = open(file_name, "w")
    ctr = 1;
    for option in list_Feasibility_output:

        text_file.write('OPTION {0}:\n'.format(ctr))
        text_file.write('Put booking ID {0} onto bus {1} \n'.format(int(URID.BookingId), option['RunID']) )
        text_file.write('Additional route time: {0} mins \n'.format(option['additional_time']/(60.0)))
        text_file.write('Additional exceeded time windows: {0} \n\n'.format(option['additional_broken_windows']))
        ctr+=1

    text_file.write('Taxi cost: {0}'.format(taxi_cost))
    text_file.close()
    return None


def preferred_options(URID_list, best_bus, delay_costs, taxi_costs, new_run_cost = None):
	'''
	Args:

	- URID_list ([]): list of all URIDs, like as outputted by get_URID_bus

	- best_bus ([]): list of buses onto which each URID would be cheapest to insert

	- delay_costs ([]]): vector of delay costs, each corresponding URID (same index as URID_list)

	- taxi_costs ([]): vector of taxi_costs, each corresponding URID (same index as URID_list)

	- new_run_cost (float): cost of sending new bus out to service all URIDs.

	WRITES: pd.DataFrame.to_csv(matrix of preferred option, per URID)'''

	bId = []; pref = []
	for i in range(len(URID)):
	    bId.append(str(int(URID[i].BookingId)))
	    if delay_costs[i] <= taxi_costs[i]:
	        pref.append(best_bus[i])
	    else:
	        pref.append('taxi')

	if new_run_cost is not None:
		bId.append('New bus option')
		pref.append('$' + str(nb_cost))

	return(pd.DataFrame(np.array([bId, pref]).T, columns = ['BookingId', 'Lowest Cost Option']))


def original_lateness(Run_Schedule, comeback1):
	'''
	Run_Schedule (pd.Dataframe) that has pickup and 

	comeback1 (int): row index in Run_Schedule corresponding to the dropoff index at which we
					 should start counting late rides'''

    bw_ctr = 0
    lateness_ctr = 0
    for k in range(comeback1, (Run_Schedule.index.max()+1)):
        if (Run_Schedule.Activity.loc[k] in [0,1]):
            bound = max(Run_Schedule.PickupEnd.loc[k], Run_Schedule.DropoffEnd.loc[k])
            eta = Run_Schedule.ETA.loc[k]
            #0 indicates TW not broken, 1 otherwise.
            bw_ctr += int(eta > bound)
            #if time window is broken, by how much?
            lateness_ctr += max(0, eta - bound)

    return({'late_windows':bw_ctr, 'total_lateness':lateness_ctr})





