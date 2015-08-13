'''Upon finding a decent fit for a URID onto a Run,
	we need to update the whole day's schedule reflecting the URID's insertion,
	and we should also write out the modified Run's new schedule.'''
import pandas as pd
import numpy as np

def day_schedule_Update(data, top_Feasibility, URID):
    '''
    data (pd.DataFrame): current schedule for all day's operations

    top_Feasibility (dict): insertion of URID on to bus resulting in min. lag.
        should be [0] element of ordered_inserts

    return (pd.DataFrame): updated (re-arranged) schedule URID properly
        put on to new bus from old bus'''

    tmp = data.copy()
    my_rows = tmp[tmp['BookingId']==URID.BookingId]
    #make sure we change the RunID of the URID when placed on new bus!
    tmp.ix[my_rows.index[:], 'Run'] = top_Feasibility['RunID']

    pickup_old = my_rows.index[0]
    dropoff_old = my_rows.index[1]
    pickup_new = top_Feasibility['pickup_insert'][1] #THIS IS OVERWRITING NEXT NODE
    dropoff_new = top_Feasibility['dropoff_insert'][1] #THIS WILL OVERWRITE NEXT NODE

    ind = tmp.index.tolist()
    ind.pop(pickup_old)
    ind.pop(dropoff_old-1)
    ind.insert(ind.index(pickup_new), pickup_old)
    ind.insert(ind.index(dropoff_new), dropoff_old)

    #move the URID into correct position in schedule
    new_data = tmp.reindex(ind)

    #update the inserted bus's ETAs!
    run_inserted = new_data[new_data['Run'] == top_Feasibility['RunID']]
    run_inserted.ix[pickup_new:dropoff_new, 'ETA'] += top_Feasibility['pickup_lag']
    run_inserted.ix[dropoff_new:, 'ETA']  += top_Feasibility['additional_time']
    new_data.ix[run_inserted.index, 'ETA'] =  run_inserted.ix[:, 'ETA']

    new_data.index = range(0, new_data.shape[0])

    return new_data


#TEST:
if __name__ == '__main__':
	import get_URIDs as gU
	import add_TimeWindowsCapacity as aTWC
	broken_Run = '2028'
	resched_init_time = 57330

	data = pd.read_csv('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/single_day_WCTW.csv')
	URID = gU.get_URID_Bus(data, broken_Run, resched_init_time)
	tF = {'total_lag': 1500, 'pickup_lag':600, 'RunID': 376, 'pickup_insert': (9,10), 'dropoff_insert': (11,12)}










