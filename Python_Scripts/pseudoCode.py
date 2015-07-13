#### Psuedo code file for Access rerouting #####
import pandas as pd
import numpy as np

broken_Run = #RunID
resched_init_time = #initial time IN SECONDS that we will begin rerouting buses. Idea is like 2hrs from breakdown time.
data_allday = pd.read_csv('./data/single_clean_day.csv', header = True) #import one day's QC'ed data
windowsz = #Variable window size

def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA. data is subsetted schedule data'''
    etas = data["ETA"]
    schtime =data["SchTime"]
    schtime[schtime<0] = np.nan
    data["Pickupwin"] = ""; data["Dropoffwin"] = "";
    for x in range(0, len(etas)):
        #dropoff window is [eta-.5*windowsize, eta+.5*windowsize]
        data["Dropoffwin"].iloc[x] = np.array([etas.iloc[x]-(windowsz/2), etas.iloc[x]+(windowsz/2)])
        data["Pickupwin"].iloc[x] = np.array([schtime.iloc[x], schtime.iloc[x]+(30*60)])
    return data


def get_URIDs(data, broken_Run, resched_init_time):
    '''get unscheduled request id's from broken bus,
        based on when we're allowed to first start rescheduling'''
    
    #all rides that exist past time we're allowed to begin rescheduling
    leftover = data[data["ETA"] >= resched_init_time]
    
    #rides that were scheduled to be on broken bus past resched_init_time
    pickmeup = leftover[leftover["Run"]==broken_Run]
    clients = pickmeup["ClientId"].unique()
    clients = clients[~(np.isnan(clients))]
    rmClients = []
    
    #remove people who would were scheduled to be on bus before resched_init_time
    for cli in clients:
        onoff = pickmeup[pickmeup["ClientId"]==cli]
        if onoff.shape[0] == 1:
            rmClients.append(cli)
    URIDs = pickmeup[~pickmeup["ClientId"].isin(rmClients)]

    unschedBag = unschedBag[unschedBag["Activity"] != 6]
    unschedBag = unschedBag[unschedBag["Activity"] != 16]
    unschedBag = unschedBag[unschedBag["Activity"] != 3]
    print("There are %s rides left to be scheduled" % pickmeup.shape[0])

    return URIDs

