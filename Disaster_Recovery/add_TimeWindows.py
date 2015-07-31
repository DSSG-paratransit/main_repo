def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA.
        data is subsetted schedule data from a day.
        windowsz is size of pickup/dropoff window in seconds'''
    
    etas = data.loc[:,"ETA"]
    schtime =data.loc[:,"SchTime"]
    schtime.loc[np.where(schtime<0)] = np.nan
    schtime.head()
    windowsz = 60*30
    sLength = data.shape[0]
    data.insert(len(data.columns), 'PickupStart',  pd.Series(np.zeros(sLength), index=data.index))
    data.insert(len(data.columns), 'PickupEnd',  pd.Series(np.zeros(sLength), index=data.index))
    data.insert(len(data.columns), 'DropoffStart',  pd.Series(np.zeros(sLength), index=data.index))
    data.insert(len(data.columns), 'DropoffEnd',  pd.Series(np.zeros(sLength), index=data.index))
    data.head(10)
    for x in range(0, sLength):

        #make dropoff window when there's no required drop off time
        if (data.Activity.loc[x] == 1) & (data.ReqLate.loc[x] <0):
            data.DropoffStart.loc[x] = data.ETA.loc[x]-3600
            data.DropoffEnd.loc[x] = data.ETA.loc[x]+3600

        #make dropoff window when there IS a required drop off time: 1hr before ReqLate time
        if (data["Activity"].loc[x] == 1) & (data["ReqLate"].loc[x] >0):
            data["DropoffStart"].loc[x] = data["ETA"].loc[x]-3600
            data["DropoffEnd"].loc[x] = data["ReqLate"].loc[x]  

        #schtime is in the middle of the pick up window
        if data["Activity"].loc[x] == 0:
            data["PickupStart"].loc[x] = schtime.loc[x]-(windowsz/2)
            data["PickupEnd"].loc[x] = schtime.loc[x]+(windowsz/2)

    return data



#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

# newdata = add_TimeWindows(data_allday, windowsz)

