import operator

class URID:
    def __init__(self, BookingId, Run, PickUpCoords, DropOffCoords, PickupStart, PickupEnd, DropoffStart, DropoffEnd, SpaceOn, MobAids, wcOn, wcOff, amOn, amOff):
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
        self.wcOn = wcOn
        self.wcOff = wcOff
        self.amOn = amOn
        self.amOff = amOff 


def get_URID_Bus(data, broken_Run, resched_init_time, add_stranded = False, BREAKDOWN_LOC = None):
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
    unsched = leftover[leftover["Run"]==broken_Run]
    diffIDs = unsched.BookingId.unique()
    diffIDs = diffIDs[~np.isnan(diffIDs)]

    print("There are %s rides left to be scheduled on broken run %s" % (unsched.shape[0], broken_Run))

    saveme = []

    #save separate URID's in a list
    for ID in diffIDs:
        my_info = unsched[unsched["BookingId"]==ID]
        #if person is already on bus when breakdown occurs,
        #need to handle URID differently:
        if(my_info.shape[0] == 1 & add_stranded):
            temp = URID(BookingId = ID,
                Run = broken_Run,
                #if person is stranded on bus, their PickUpCoords are the BREAKDOWN_LOC (global var)
                PickUpCoords = pd.Series(data = np.array(BREAKDOWN_LOC), index = ["LAT", "LON"]),
                DropOffCoords = my_info[["LAT", "LON"]].ix[0,],
                PickupStart = resched_init_time,
                PickupEnd = resched_init_time+30*60,
                DropoffStart = int(my_info[["DropoffStart"]].ix[0,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].ix[0,]),
                SpaceOn = my_info[["SpaceOn"]].ix[0,],
                MobAids = my_info[["MobAids"]].ix[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,]))
        if(my_info.shape[0] != 1):
            temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = my_info[["LAT", "LON"]].ix[0,],
                DropOffCoords = my_info[["LAT", "LON"]].ix[1,],
                PickupStart = int(my_info[["PickupStart"]].ix[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].ix[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].ix[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].ix[1,]),
                SpaceOn = my_info[["SpaceOn"]].ix[0,],
                MobAids = my_info[["MobAids"]].ix[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,]))
        
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
        my_info = data[data["BookingId"]==ID]
        temp = URID(BookingId = ID,
                Run = broken_Run,
                PickUpCoords = my_info[["LAT", "LON"]].iloc[0,],
                DropOffCoords = my_info[["LAT", "LON"]].iloc[1,],
                PickupStart = int(my_info[["PickupStart"]].iloc[0,]),
                PickupEnd = int(my_info[["PickupEnd"]].iloc[0,]),
                DropoffStart = int(my_info[["DropoffStart"]].iloc[1,]),
                DropoffEnd = int(my_info[["DropoffEnd"]].iloc[1,]),
                SpaceOn = my_info[["SpaceOn"]].iloc[0,],
                MobAids = my_info[["MobAids"]].iloc[0,],
                wcOn = my_info["wcOn"].ix[0,],
                wcOff = my_info["wcOff"].ix[0,],
                amOn = my_info["amOn"].ix[0,],
                amOff = my_info["amOff"].ix[0,])
)
        
        saveme.append(temp)

    #return sorted URIDs based on PickupStart time
    return sorted(saveme, key = operator.attrgetter('PickupStart'))







