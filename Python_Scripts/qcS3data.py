'''
What this script does:
Access the S3 paratransitdata bucket, download the relevant real-time file as "real_time_data.csv"

command-line arguments: argv[1] = AWS_ACCESS_KEY, argv[2] = AWS_SECRET_KEY

File management: make sure you're in the directory containing the location of the data files,
	path_to_data, and you will write the full path to the read_fwf.py script.
'''

import sys
import re
import time
import os
import pandas as pd

path_to_data = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/'
os.chdir(path_to_data)
qc_file_name = path_to_data+'qc_streaming.csv'
if 'qc_streaming.csv' in os.listdir(os.getcwd()):
    os.remove(qc_file_name)

#For establishing connection, use access and secret keys sent by Valentina.
#aws access key: sys.argv[1]
#aws secret key: sys.argv[2]


#STEP 1: Access S3 and download relevant streaming data file
from boto.s3.connection import S3Connection
conn = S3Connection(sys.argv[1], sys.argv[2])

conn.get_all_buckets()

bucket = conn.get_bucket('paratransitdata')

#print bucket contents:
rs = bucket.list()

#get list of streaming_data files for today's date
file_ls = []
for key in rs:
    if re.search("streaming_data/Schedules_"+ time.strftime('%Y%m%d'),key.name.encode('ascii')):
        file_ls.append(key.name.encode('ascii'))

#select relevant streaming_data file:
data_key = bucket.get_key(file_ls[-1])
move_to_me = 'real_time_data.csv'
data_key.get_contents_to_filename(move_to_me)


#STEP 2: change this file from fixed width formatted to tab delimitted
sys.argv = ['read_fwf.py','real_time_data.csv', 'real_time_tab.csv']
execfile('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Python_Scripts/read_fwf.py')

#STEP 3: QC this file a la the R QCing script
data = pd.read_csv('real_time_tab.csv', sep = '\t')


data56 = data.loc[(data.ProviderId == 5) | (data.ProviderId == 6)]
rides = data56.Run.unique()
data56.ix[:,'Activity'] = data56.ix[:,'Activity'].astype('int')

#lat/lon constraints:
upper_right = [49.020430, -116.998768]
lower_left = [45.606961, -124.974842]
minlat = lower_left[0]; maxlat = upper_right[0]
minlon = lower_left[1]; maxlon = upper_right[1]


#Write the cleaned up data:
ctr = 0
for ride in rides:
    temp_ride = data56.loc[data56.Run == ride]
    temp_ride.drop(temp_ride.columns[0], axis = 1)
    
    flag = 1 #1 == good, 0 == eliminate.
    lats = temp_ride.LAT; lons = temp_ride.LON
    #eliminate runs from roster that have bad lat/lon data:
    if(any(lats < minlat) | any(lats>maxlat) | any(lons<minlon) | any(lons > maxlon)):
        flag = 0
    #eliminate runs that don't move
    if(all(lats == lats.iloc[0]) | all(lons == lons.iloc[0])):
        flag = 0
    #eliminate runs that don't leave a garage and return to a garage
    if (temp_ride.Activity.iloc[0] != 4.) | (temp_ride.Activity.iloc[-1] != 3.):
        flag = 0
        
    temp_ride = temp_ride.drop(temp_ride.columns[0], axis = 1)
    
    if (ctr == 0) & (flag == 1):
        temp_ride.to_csv(qc_file_name, mode = 'a', header = True, index = False)
        ctr +=1
    if (ctr != 0) & (flag == 1) :
        temp_ride.to_csv(qc_file_name, mode = 'a', header = False, index = False)










