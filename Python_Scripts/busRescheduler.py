import numpy as np
import pandas as pd
import sys
import get_URIDS as g_u
import Feasibility as Feasibility
import runUpdater as rUp

"""
sys.argv[1] is path to csv file for day's schedule
sys.argv[2] is int for time window in seconds
sys.argv[3] is str for broken bus run number, OR, it is a list of bookingId's (for single client input)
sys.argv[4] is int for time in seconds (this should be changed to accept more user friendly input)

eventually make function(?) which makes sure user is passing correct num/type of arguments.
For now, enter None when you don't want to input a command line argument.

"""

# all try except statements are prompting the user for the needed input  

#Get data   
try:
    fullSchedule = pd.DataFrame.from_csv(sys.argv[1], header=0, sep=',')

except IOError:
    #grab s3 streaming_data/ file if no file specified
    print "File does not exist."
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

#Get time window size
windows = sys.argv[2]
if windows is None:
    windows = 1800

#Determine broken run number, or get list of unhandled requests.
broken_Run = sys.argv[3]
if broken_Run is None:
    broken_Run = input("Please enter broken bus ID number as a string, OR, input a list of unhandled BookingIds: ")
    if type(broken_Run) == str:
        case = 'BROKEN_RUN' 
    else:
        case = 'INDIVIDUAL_REQUESTS'
        individual_requests = broken_Run

resched_init_time = sys.argv[4]
if resched_init_time is None:
    try:
        resched_init_time = humanToSeconds(sys.argv[4])
    except ValueError:
        print('Please enter a break-down time according to the prompt!\n')
        resched_init_time = humanToSeconds(sys.argv[4])



# eventually add_timeWindows should also add capacity columns (not yet integrated)
# this simply returns full schedule with time windows at the moment 
fullSchedule_windows = add_TimeWindows(fullSchedule,windows)
fS_w_copy = fullSchedule_windows.copy()

# this gets us all the URIDs for the broken run given the initial rescheduling time 
# OR it will get us URIDs given specific bookingIds to be rescheduled
if case == 'BROKEN_RUN':
    URIDs = g_u.get_URID_Bus(fullSchedule_windows, broken_Run)
else:
    URIDs = g_u.get_URID_BookingIds(individual_requests)

# for each URID we find the bus runs to check through a radius elimination.
# for each URID for each run we then want to check the capacity in the given time
# window and return the URID with updated insert points. This URID with updated
# insert points is fed to the feasibilty function, which we ultimately want to return
# a minimum cost run for the URID and that run updated with the new URID slotted in.
cost_dict = {} #dictionary that will store, by BookingId key, the cost for inserting client into
# new run as well as that run number 

delay_cost = 0
for i in range(len(URIDs)):
    busRuns_tocheck = radius_Elimination(fullSchedule_windows, URIDs[i], radius=5.)
    insert_stats = []
    for run in busRuns_tocheck:
        URID_updated_insertpts = checkCapacityInsertPts(URIDs[i],run)
        runSchedule = get_busRuns(fullSchedule_windows, run, None)
        brokenwindows_dict =Feasibility.insertFeasibility(runSchedule, URID_updated_insertpts)
        insert_stats.append(brokenwindows_dict)

    #order buses by lowest additional lag time, i.e. total_lag, and sequentially add total_lag's
    ordered_inserts = sorted(insert_stats.items(), key = operator.itemgetter('total_lag'))
    delay_cost += ordered_inserts['total_lag']*(48.09/3600)

    #calculate taxi cost
    taxi_cost = taxi(URIDs[i].PickUpCoords.LAT, URIDs[i].PickUpCoords.LON,
        URIDs[i].DropOffCoords.LAT, DropOffCoords.LON, wheelchair_present(URIDs[i]))
    #write information about best insertions to text file
    rUp.write_insert_data(URID, ordered_inserts[0:3],
        '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output/', taxi_cost)
    #update whole day's schedule:
    fullSchedule_windows = rUp.day_schedule_Update(fullSchedule_windows, ordered_inserts[0], URIDs[i])

#Calculate new bus's cost, ONLY IN CASE OF BROKEN BUS:
if case == 'BROKEN_RUN':
    newRun_cost = newBusRun_cost(get_busRuns(fS_w_copy, broken_Run, URID):, provider)
    # for provider we need to check availability of buses and compare costs---^^^
    print('Cost of sending new bus for broken run {0} is {1}.'.format(brokenRun, newBusRun_cost))

print('Cost of rerouting all URIDs is {0}'.format(delay_cost*(48.09/3600)))

fullSchedule_windows.to_csv('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output/newSchedule.csv', index = False)

return None

    
