def get_URIDs(data, broken_Run, resched_init_time):
    '''get unscheduled request id's from broken bus,
        based on when we're allowed to first start rescheduling.
        resched_init_time is in seconds, marks the point in time we can begin considering reinserting new requests.
        broken_Run is number of run that breaks
        data is today's scheduling data

        RETURN: list of URIDs'''
    
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
    unsched = pickmeup[~pickmeup["ClientId"].isin(rmClients)]

    print("There are %s rides left to be scheduled" % unsched.shape[0])

    class URID:
        def __init__(self, BookingId, Run, PickUpCoords, DropOffCoords, PickupStart, PickupEnd, DropoffStart, DropoffEnd, SpaceOn, MobAids):
            self.BookingId= BookingId
            self.Run = Run
            self.PickUpCoords = PickUpCoords
            self.DropOffCoords = DropOffCoords
            self.PickupStart = PickupStart
            self.PickupEnd = PickupEnd
            self.DropoffStart = DropoffStart
            self.DropoffEnd = DropoffEnd
            self.SpaceOn = SpaceOn
            self.MobAids = MobAids


    diffIDs = unsched.BookingId.unique()
    saveme = []

    #save separate URID's in a list
    for ID in diffIDs:
        temp = URID(BookingId = ID,
            Run = broken_Run,
            PickUpCoords = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["LAT", "LON"]].iloc[0,],
            DropOffCoords = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["LAT", "LON"]].iloc[1,],
            PickupStart = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["PickupStart"]],
            PickupEnd = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["PickupEnd"]],
            DropoffStart = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["PickupEnd"]],
            DropoffEnd = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["PickupEnd"]],
            SpaceOn = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["SpaceOn"]].iloc[0,],
            MobAids = unsched[unsched["BookingId"]==unsched.BookingId.iloc[0]][["MobAids"]].iloc[0,])
        saveme.append(temp)

    return saveme

#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day_TimeWindows.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#broken_Run = 508 #RunID
#resched_init_time = 800*60 #initial time IN SECONDS that we will begin rerouting buses. Idea is like 2hrs from breakdown time.

# URIDs = get_URIDs(data_allday, broken_Run, resched_init_time)

