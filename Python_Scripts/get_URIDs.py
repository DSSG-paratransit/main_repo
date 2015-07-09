def get_URIDs(data, broken_Run, resched_init_time):
    '''get unscheduled request id's from broken bus,
        based on when we're allowed to first start rescheduling.
        resched_init_time is in seconds, marks the point in time we can begin considering reinserting new requests.
        broken_Run is number of run that breaks
        data is today's scheduling data'''
    
    #all rides that exist past time we're allowed to begin rescheduling
    leftover = data[data["ETA"] >= resched_init_time]
    leftover = leftover[(leftover["Activity"] != 6) & (leftover["Activity"] != 16) & (leftover["Activity"] != 3)]
    
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

    print("There are %s rides left to be scheduled" % URIDs.shape[0])

    return URIDs

#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#broken_Run = #RunID
#resched_init_time = 800*60 #initial time IN SECONDS that we will begin rerouting buses. Idea is like 2hrs from breakdown time.

# URIDs = get_URIDs(data_allday, broken_Run, resched_init_time)

