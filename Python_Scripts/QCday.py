import pandas as pd
import numpy as np
from datetime import datetime

#test date for insertion
testdate = datetime.strptime("4/14/2014", "%m/%d/%Y")

#grab lines 700,000 through 800,000 from 18 month data file with headers
data = pd.read_csv("/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/UW_Trip_Data_FullHeaders.csv",
                   header = True, skiprows = np.union1d(range(0,700000), range(800001, 3493640)))
headers = ["ServiceDate", "Run", "ProviderId", "EvOrder", "EvId", "ReqTime",
           "SchTime", "ReqLate", "Activity", "ETA", "DwellTime", "StreetNo",
           "OnStreet", "City", "LON", "LAT", "BookingId", "SchedStatus", "SubtypeAbbr","FundingSourceId1",
           "PassOn", "SpaceOn", "PassOff", "SpaceOff", "ClientId", "MobAids"]
data.columns = headers
data.ClientId = np.int64(data.ClientId)
data.ServiceDate = [datetime.strptime(data.ServiceDate[i], "%m/%d/%Y %H:%M:%S") for i in range(0, data.shape[0])]
Apr_14 =data[(data["ServiceDate"] == testdate) & ((data["ProviderId"]==6) | (data["ProviderId"]==5))]