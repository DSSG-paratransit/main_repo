#Run busRescheduler from command line. Run these lines in a python environment.

import subprocess
args = ['python', 'busRescheduler.py', '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output/qc_streaming_DEMO.csv', 'None', 'None', '6020', '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output', '11:30', 'None', '1800.', '3.']

p = subprocess.Popen(args)