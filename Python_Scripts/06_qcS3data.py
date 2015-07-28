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
rides = data.Run.unique()

#lat/lon constraints:
upper_right <- [49.020430, -116.998768]
lower_left <- [45.606961, -124.974842]
minlat = lower_left[0]; maxlat = upper_right[0]
minlon = lower_left[1]; maxlon = upper_right[1]

for ride in rides:







