'''Upon finding a decent fit for a URID onto a Run,
	we need to update the whole day's schedule reflecting the URID's insertion,
	and we should also write out the modified Run's new schedule.'''


def write_insert_data(URID, list_Feasibility_output, path_to_output):
	'''
		list_Feasibility_output (list of dicts): some of the top insertion options from busRescheduler loop that are assembled
		into a list (like 'ordered_inserts' in busRescheduler),
		write out some of the information about the insertion (lag, number of late windows, average lateness)'''

	file_name = path_to_output + str(int(URID.BookingId)) + '_insert_data.txt'
	text_file = open(file_name, "w")
	for option in list_Feasibility_output:
		number_late = sum(option['score']['break_TW'].tolist())
		avg_late = sum(option['score']['late'].tolist())/number_late

		text_file.write('OPTION 1:\n')
		text_file.write('Put {0} onto bus {1} \n'.format(int(URID.BookingId), option['RunID']) )
		text_file.write('Total lag: {0} \n'.format(int(option['total_lag'])))
		text_file.write('Number of exceeded time windows: {0} \n'.format()
		text_file.write('Average lateness: {0} \n\n\n'.format(avg_late))

	text_file.close()
	return None


def day_schedule_Update(data, top_Feasibility, URID):
	'''
	data (pd.DataFrame): current schedule for all day's operations

	top_Feasibility (dict): insertion of URID on to bus resulting in min. lag.
		should be [0] element of ordered_inserts

	return (pd.DataFrame): updated (re-arranged) schedule URID properly
		put on to new bus from old bus'''

	tmp = data.copy()

	my_rows = tmp[tmp['BookingId']==URID.BookingId]
	p_ind_old = my_rows.index[0]; d_ind_old = my_rows.index[1]
	p_ind_new = top_Feasibility['pickup_insert'][1] #Swap with p_ind_old
	d_ind_new = top_Feasibility['dropoff_insert'][1] #Swap with d_ind_old

	ind = tmp.index.tolist()
	a_p, b_p = ind.index(p_ind_old), ind.index(p_ind_new)
	a_d, b_d = ind.index(d_ind_old), ind.index(d_ind_new)
	ind[a_p], ind[b_p] = ind[b_p], ind[a_p]
	ind[a_d], ind[b_d] = ind[b_d], ind[a_d]
	
	return tmp.reindex(ind)












