'''
What this script does:
Access the S3 paratransitdata bucket, download the relevant real-time file as "real_time_data.csv"

command-line arguments: argv[1] = AWS_ACCESS_KEY, argv[2] = AWS_SECRET_KEY
'''

import sys
import re
import time

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
move_to_me = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/real_time_data.csv'
data_key.get_contents_to_filename(move_to_me)


#STEP 2: QC this file 


