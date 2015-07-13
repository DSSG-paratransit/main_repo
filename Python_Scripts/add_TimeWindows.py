def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA.
        data is subsetted schedule data from a day.
        windowsz is size of pickup/dropoff window in seconds'''

    etas = data["ETA"]
    schtime =data["SchTime"]
    schtime[schtime<0] = np.nan
    data["PickupStart"] = 0; data["PickupEnd"] = 0
    data["DropoffStart"] = 0; data["DropoffEnd"] = 0
    for x in range(0, len(etas)):

        #make dropoff window when there's no required drop off time
        if (data["Activity"].iloc[x] == 1) & (data["ReqLate"].iloc[x] <0):
            data["DropoffStart"].iloc[x] = data["ETA"].iloc[x]-3600
            data["DropoffEnd"].iloc[x] = data["ETA"].iloc[x]+3600
        
        #make dropoff window when there IS a required drop off time: 1hr before ReqLate time
        if (data["Activity"].iloc[x] == 1) & (data["ReqLate"].iloc[x] >0):
            data["DropoffStart"].iloc[x] = data["ETA"].iloc[x]-3600
            data["DropoffEnd"].iloc[x] = data["ReqLate"].iloc[x]  
        
        #schtime is in the middle of the pick up window
        if data["Activity"].iloc[x] == 0:
            data["PickupStart"].iloc[x] = schtime.iloc[x]-(windowsz/2)
            data["PickupEnd"].iloc[x] = schtime.iloc[x]+(windowsz/2)

    return data



#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

# newdata = add_TimeWindows(data_allday, windowsz)

