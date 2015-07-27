import numpy as np
import pandas as pd
import sys

"""
sys.argv[1] is path to csv file for day's schedule
sys.argv[2] is int for time window in seconds
sys.argv[3] is str for broken bus run number 
sys.argv[4] is int for time in seconds (this should be changed to accept more user friendly input)

eventually make function(?) which makes sure user is passing correct num/type of arguments

"""

# all try except statements are prompting the user for the needed input     
try:
    fullSchedule = pd.DataFrame.from_csv(sys.argv[1], header=0, sep=',')
except IndexError:
    print "Please input path to csv file that contains day's schedule."
    quit()
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
URIDs = get_URIDs(fullSchedule_windows, broken_Run, resched_init_time)

# for each URID we find the bus runs to check through a radius elimination.
# for each URID for each run we then want to check the capacity in the given time
# window and return the URID with updated insert points. This URID with updated
# insert points is fed to the feasibilty function, which we ultimately want to return
# a minimum cost run for the URID and that run updated with the new URID slotted in. 
for URID in URIDS:
    busRuns_tocheck = radius_Elimination(fullSchedule_windows, URID, radius=5., pickUpDropOff=True)

    cost_array  = [] #this is incorrect as it stands right now as they get overwritten
    run_array  = [] #this is incorrect as it stands right now as they get overwritten
    for run in busRuns_tocheck:
        URID_updated_insertpts = checkCapacityInsertPts(URID,run)
        brokenwindows_dict =Feasibility.insertFeasibility(run,URID_updated_insertpts)
        cost_array = np.append(score_array, brokenwindows_dict['total_lag'])
        run_array = np.append(run_array,run)

    min_cost = np.min(cost_array)*(48./3600)
    run_wmin_cost = run_array[np.where(cost_array == min_cost)]
