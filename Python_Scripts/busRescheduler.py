import numpy as np
import pandas as pd
import sys
import get_URIDS as g_u
import Feasibility as Feasibility

"""
sys.argv[1] is path to csv file for day's schedule
sys.argv[2] is int for time window in seconds
sys.argv[3] is str for broken bus run number, OR, it is a list of bookingId's (for single client input)
sys.argv[4] is int for time in seconds (this should be changed to accept more user friendly input)

eventually make function(?) which makes sure user is passing correct num/type of arguments

"""

# all try except statements are prompting the user for the needed input     
try:
    fullSchedule = pd.DataFrame.from_csv(sys.argv[1], header=0, sep=',')

except IndexError:
    #grab s3 streaming_data/ file if no file specified
    result = None
    while result is None:
        try:
            qc_file_path = input("Please enter full path to the S3/QC script: ")
            AWS_ACCESS_KEY = input("Please enter AWS access key: ")
            AWS_SECRET_KEY = input("Please enter AWS secret key: ")
            subprocess.call([qc_file_path, AWS_ACCESS_KEY, AWS_SECRET_KEY])
            path_to_data = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/qc_streaming.csv'
            result = pd.read_csv(path_to_data)
            fullSchedule = result
        except:
            pass

except IOError:
    print "File does not exist."
    quit()

try:
    windows = sys.argv[2]
except IndexError:
    windows = 1800

try:
    broken_Run = sys.argv[3]
except IndexError:
    print "Please enter broken bus ID number"
    quit()

try:
    resched_init_time = humanToSeconds(sys.argv[4])
except IndexError:
    print "Please enter initial time at which to begin rescheduling."
    quit()
except ValueError:
    print "Please enter a valid time in HH:MM format."
    quit()


# eventually add_timeWindows should also add capacity columns (not yet integrated)
# this simply returns full schedule with time windows at the moment 
fullSchedule_windows = add_TimeWindows(fullSchedule,windows)

# this gets us all the URIDs for the broken run given the initial rescheduling time 
# OR it will get us URIDs given specific bookingIds to be rescheduled
if type(sys.argv[3]) == str:
    URIDs = g_u.get_URID_Bus(fullSchedule_windows, broken_Run)
else:
    URIDs = g_u.get_URID_BookingIds(sys.argv[3])

# for each URID we find the bus runs to check through a radius elimination.
# for each URID for each run we then want to check the capacity in the given time
# window and return the URID with updated insert points. This URID with updated
# insert points is fed to the feasibilty function, which we ultimately want to return
# a minimum cost run for the URID and that run updated with the new URID slotted in.
cost_dict = {} #dictionary that will store, by BookingId key, the cost for inserting client into
# new run as well as that run number 

overall_lag = 0 #keep track of overall lag from rerouting buses for all URIDs
best_inserts = [] #for each URID, keep track of stats re: best insertion on to existing schedule
for i in range(len(URIDs)):
    busRuns_tocheck = radius_Elimination(fullSchedule_windows, URIDs[i], radius=5.)
    insert_stats = []
    for run in busRuns_tocheck:
        URID_updated_insertpts = checkCapacityInsertPts(URIDs[i],run)
        runSchedule = get_busRuns(fullSchedule_windows, run)
        brokenwindows_dict =Feasibility.insertFeasibility(runSchedule, URID_updated_insertpts)
        insert_stats.append(brokenwindows_dict)

    ordered_inserts = sorted(insert_stats.items(), key = operator.itemgetter('total_lag'))
    overall_lag += ordered_inserts[0]['total_lag']
    best_inserts.append(ordered_inserts[0])




min_cost = np.min([cost_dict[key]['Cost'] for key in cost_dict])*(48.09/3600)
min_cost_run = [cost_dict[key]['Run'] for key in cost_dict if cost_dict[key]['Cost'] == min_cost]
    
