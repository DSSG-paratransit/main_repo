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


def get_URID_Bus(data, broken_Run, resched_init_time):
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
    unsched = pickmeup

    print("There are %s rides left to be scheduled on broken run %s" % (unsched.shape[0], broken_Run))

    diffIDs = unsched.BookingId.unique()
    saveme = []

    #save separate URID's in a list
    for ID in diffIDs:
        my_info = unsched[unsched["BookingId"]==ID]
        #if person is already on bus when breakdown occurs,
        #need to handle URID differently:
        if(my_info.shape[0] == 1):
            temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = pd.Series(data = np.array(BREAKDOWN_LOC), index = ["LAT", "LON"]),
                DropOffCoords = my_info[["LAT", "LON"]].iloc[0,],
                PickupStart = resched_init_time,
                PickupEnd = resched_init_time+30*60,
                DropoffStart = int(my_info[["DropoffStart"]].iloc[0,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].iloc[0,]),
                SpaceOn = my_info[["SpaceOn"]].iloc[0,],
                MobAids = my_info[["MobAids"]].iloc[0,])
        else:
            temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = my_info[["LAT", "LON"]].iloc[0,],
                DropOffCoords = my_info[["LAT", "LON"]].iloc[1,],
                PickupStart = int(my_info[["PickupStart"]].iloc[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].iloc[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].iloc[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].iloc[1,]),
                SpaceOn = my_info[["SpaceOn"]].iloc[0,],
                MobAids = my_info[["MobAids"]].iloc[0,])
        
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


def get_URID_BookingIds(data, BookingId_list):
    '''get unscheduled request id's from broken bus,
    based on the list of BookingIds provided by dispatcher

    RETURN: list of URIDs'''

    diffIDs = BookingId_list
    saveme = []
    for ID in diffIDs:
        my_info = unsched[unsched["BookingId"]==ID]
        temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = my_info[["LAT", "LON"]].iloc[0,],
                DropOffCoords = my_info[["LAT", "LON"]].iloc[1,],
                PickupStart = int(my_info[["PickupStart"]].iloc[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].iloc[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].iloc[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].iloc[1,]),
                SpaceOn = my_info[["SpaceOn"]].iloc[0,],
                MobAids = my_info[["MobAids"]].iloc[0,])
        
        saveme.append(temp)

    return saveme







