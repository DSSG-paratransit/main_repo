'''Upon finding a decent fit for a URID onto a Run,
	we need to update the whole day's schedule reflecting the URID's insertion,
	and we should also write out the modified Run's new schedule.'''
import pandas as pd
import numpy as np

def write_insert_data(URID, list_Feasibility_output, path_to_output):
	'''
		list_Feasibility_output (list of dicts): some of the top insertion options from busRescheduler loop that are assembled
		into a list (like 'ordered_inserts' in busRescheduler)


		taxi_cost (double): cost of sending URID to taxi

		goal: write out some of the information about the insertion (lag, number of late windows, average lateness)'''

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

	text_file.write('Taxi cost: {0}'.format(taxi_cost))
	text_file.close()
	return None


def day_schedule_Update(data, top_Feasibility, URID, taxi_cost):
	'''
	data (pd.DataFrame): current schedule for all day's operations

	top_Feasibility (dict): insertion of URID on to bus resulting in min. lag.
		should be [0] element of ordered_inserts

	return (pd.DataFrame): updated (re-arranged) schedule URID properly
		put on to new bus from old bus'''

	tmp = data.copy()
	my_rows = data[data['BookingId']==URID.BookingId]
	#make sure we change the RunID of the URID when placed on new bus!
	tmp.ix[my_rows.index[:], 'Run'] = top_Feasibility['RunID']

	pickup_old = my_rows.index[0]
	dropoff_old = my_rows.index[1]
	pickup_new = ret['pickup_insert'][1] #THIS IS OVERWRITING NEXT NODE
	dropoff_new = ret['dropoff_insert'][1] #THIS WILL OVERWRITE NEXT NODE

	ind = test.index.tolist()
	ind.pop(pickup_old)
	ind.pop(dropoff_old-1)
	ind.insert(ind.index(pickup_new), pickup_old)
	ind.insert(ind.index(dropoff_new), dropoff_old)

	#move the URID into correct position in schedule
	new_data = tmp.reindex(ind)

	#update the inserted bus's ETAs!
	run_inserted = new_data[new_data['Run'] == URID.Run]
	run_inserted.ix[pickup_new:dropoff_new, 'ETA'] = etas + top_Feasibility['pickup_lag']
	run_inserted.ix[dropoff_new:, 'ETA'] = etas + top_Feasibility['total_lag']
	new_data.ix[run_inserted.index, 'ETA'] =  run_inserted.ix[:, 'ETA']

	return new_data


if __name__ == '__main__':
	import get_URIDs as gU
	broken_bus = '403R'
	resched_init_time = 63500

	data = pd.read_csv('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/single_day_TimeWindows.csv')
	URID = gU.get_URIDs(data, broken_bus, resched_init_time)
	tF = {'total_lag': 1500, 'pickup_lag':600, 'RunID': 376}










