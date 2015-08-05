def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA.
        data is subsetted schedule data from a day.
        windowsz is size of pickup/dropoff window in seconds'''

    data.index = range(0, data.shape[0])

    etas = data.ix[:,"ETA"]
    schtime =data.ix[:,"SchTime"]
    Activity = data.ix[:, "Activity"]
    ReqLate = data.ix[:, "ReqLate"]

    schtime_arr = np.array(schtime.tolist())
    nrow = data.shape[0]
    PickupStart = np.zeros(nrow); PickupEnd = np.zeros(nrow)
    DropoffStart = np.zeros(nrow); DropoffEnd = np.zeros(nrow)

    for x in range(0, nrow):

        #make dropoff window when there's no required drop off time
        if (Activity[x] == 1) & (ReqLate[x] <0):
            DropoffStart[x] = etas[x]-3600
            DropoffEnd[x] = etas[x]+3600

        #make dropoff window when there IS a required drop off time: 1hr before ReqLate time
        if (Activity[x] == 1) & (ReqLate[x] >0):
            DropoffStart[x] = etas[x]-3600
            DropoffEnd[x] = ReqLate[x]  

        #schtime is in the middle of the pick up window
        if Activity[x] == 0:
            PickupStart[x] = schtime[x]-(windowsz/2)
            PickupEnd[x] = schtime[x]+(windowsz/2)
        
    data.insert(len(data.columns), 'PickupStart',  pd.Series((PickupStart), index=data.index))
    data.insert(len(data.columns), 'PickupEnd',  pd.Series((PickupEnd), index=data.index))
    data.insert(len(data.columns), 'DropoffStart',  pd.Series(DropoffStart, index=data.index))
    data.insert(len(data.columns), 'DropoffEnd',  pd.Series(DropoffEnd, index=data.index))

    return data.copy()



#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

# newdata = add_TimeWindows(data_allday, windowsz)

