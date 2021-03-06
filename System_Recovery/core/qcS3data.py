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
import read_fwf

def s3_data_acquire(AWS_ACCESS_KEY, AWS_SECRET_KEY, path_to_data, qc_file_name = 'qc_streaming.csv'):

    '''
    For establishing connection, use access and secret keys sent by Valentina.
    '''
    if os.path.isfile(os.path.join(path_to_data, qc_file_name)):
        os.remove(os.path.join(path_to_data, qc_file_name))

    #STEP 1: Access S3 and download relevant streaming data file
    from boto.s3.connection import S3Connection
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    conn.get_all_buckets()

    bucket = conn.get_bucket('paratransitdata')

    #print bucket contents:
    rs = bucket.list()

    #get list of streaming_data files for today's date
    file_ls = []
    for key in rs:
        if re.search('streaming_data/Schedules_'+ time.strftime('%Y%m%d'),key.name.encode('ascii')):
            file_ls.append(key.name.encode('ascii'))

    if not file_ls:
        print('There are no files from '+ str(time.strftime('%Y/%m/%d'))+ '!')
        return -1
        quit()
        
    #select relevant streaming_data file: watch out, hopefully the [-1] file isn't zero bytes!
    data_key = bucket.get_key(file_ls[-1])
    move_to_me = os.path.join(path_to_data,'real_time_data.tsv')
    data_key.get_contents_to_filename(move_to_me)
    print('Saving {0} from S3 bucket.'.format(file_ls[-1]))

    #STEP 2: change this file from fixed width formatted to tab delimitted
    data = read_fwf.read(move_to_me)
    print('Successfully converted fwf file.')

    #STEP 3: QC this file a la the R QCing script

    data56 = data.loc[(data.ProviderId == 5.) | (data.ProviderId == 6.)]
    rides = data56.Run.unique()
    data56.loc[:,'Activity'] = data56.loc[:,'Activity'].astype('int')

    #lat/lon constraints:
    upper_right = [49.020430, -116.998768]
    lower_left = [45.606961, -124.974842]
    minlat = lower_left[0]; maxlat = upper_right[0]
    minlon = lower_left[1]; maxlon = upper_right[1]


    #Write the cleaned up data:
    ctr = 0
    qc_file_name = os.path.join(path_to_data, qc_file_name)
    for ride in rides:
        temp_ride = data56.loc[data56.Run == ride]
        if 'ServiceDate' in temp_ride.columns:
            temp_ride = temp_ride.drop('ServiceDate', axis = 1)
        
        flag = 1 #1 == good, 0 == eliminate.
        lats = temp_ride.LAT; lons = temp_ride.LON
        #eliminate runs from roster that have bad lat/lon data:
        if(any(lats < minlat) | any(lats>maxlat) | any(lons<minlon) | any(lons > maxlon)):
            flag = 0
        #eliminate runs with just 2 rows of data:
        if temp_ride.shape[0] == 2:
            flag = 0
        #eliminate runs that don't move
        if(all(lats == lats.iloc[0]) | all(lons == lons.iloc[0])):
            flag = 0
        #eliminate runs that don't leave a garage and return to a garage
        if (temp_ride.Activity.iloc[0] != 4) | (temp_ride.Activity.iloc[-1] != 3):
            flag = 0

        if (ctr != 0) & (flag == 1) :
            temp_ride.to_csv(qc_file_name, mode = 'a', header = False, index = False)
        if (ctr == 0) & (flag == 1):
            temp_ride.to_csv(qc_file_name, mode = 'a', header = True, index = False)
            ctr = 1

    read_me = os.path.join(path_to_data, qc_file_name)
    ret = pd.read_csv(read_me)
    
    #resolve indexing issues if index column is type timedate, or something else
    if not set(ret.index)==set(range(0, ret.shape[0])):
        ret.index = range(0, ret.shape[0])
    
    return ret


def main():
    AWS_ACCESS_KEY = raw_input('Please enter AWS access key: ')
    AWS_SECRET_KEY = raw_input('Please enter AWS secret access key: ')
    path_to_data = raw_input('Please enter path to data output directory: ')
    test_data = s3_data_acquire(AWS_ACCESS_KEY, AWS_SECRET_KEY, path_to_data, qc_file_name = 'qc_streaming.csv')
    print('Successfully downloaded and QCed streaming_data.')

if __name__ == "__main__":
    main()

else:
    print('Importing qcS3data')








