def write_insert_data(URID, list_Feasibility_output, path_to_output):
	'''
		list_Feasibility_output (list of dicts): some of the top insertion options from busRescheduler loop that are assembled
		into a list (like 'ordered_inserts' in busRescheduler)


		taxi_cost (double): cost of sending URID to taxi

		goal: write out some of the information about the insertion (lag, number of late windows, average lateness)'''

	file_name = os.path.join(path_to_output, str(int(URID.BookingId)), '_insert_data.txt')
	text_file = open(file_name, "w")
	ctr = 1
	for option in list_Feasibility_output:
		number_late = sum(option['score']['break_TW'].tolist())
		avg_late = sum(option['score']['late'].tolist())/number_late

		text_file.write('OPTION {0}:\n'.format{0})
		text_file.write('Put {0} onto bus {1} \n'.format(int(URID.BookingId), option['RunID']) )
		text_file.write('Total lag: {0} \n'.format(int(option['total_lag'])))
		text_file.write('Number of exceeded time windows: {0} \n'.format()
		text_file.write('Average lateness: {0} \n\n\n'.format(avg_late))

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






