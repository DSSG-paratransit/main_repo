def add_TimeWindows(data, windowsz):
    '''calculate time windows (pickup and dropoff)
        from SchTime and ETA.
        data is subsetted schedule data from a day.
        windowsz is size of pickup/dropoff window in seconds'''

    etas = data["ETA"]
    schtime =data["SchTime"]
    schtime[schtime<0] = np.nan
    data["Pickupwin"] = ""; data["Dropoffwin"] = "";
    for x in range(0, len(etas)):
        #dropoff window is [eta-.5*windowsize, eta+.5*windowsize]
        data["Dropoffwin"].iloc[x] = np.array([etas.iloc[x]-(windowsz/2), etas.iloc[x]+(windowsz/2)])
        data["Pickupwin"].iloc[x] = np.array([schtime.iloc[x], schtime.iloc[x]+(30*60)])
    return data



#TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

# newdata = add_TimeWindows(data_allday, windowsz)

