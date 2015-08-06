import all_functions as af

"""
    sys.argv[1] is path to csv file for day's schedule
    sys.argv[2] is int for time window in seconds
    sys.argv[3] is str for broken bus run number, OR, it is a list of bookingId's (for single client input)
    sys.argv[4] is int for time in seconds (this should be changed to accept more user friendly input)
    sys.argv[5] is str for path to directory where you want the output .txt/.csv files to go
    
    eventually make function(?) which makes sure user is passing correct num/type of arguments.
    For now, enter None when you don't want to input a command line argument.
    
    """

# all try except statements are prompting the user for the needed input

#Get data
#Get data


try:
    fullSchedule = af.pd.DataFrame.from_csv(af.sys.argv[1], header=0, sep=',')

except IOError:
    #grab s3 streaming_data/ file if no file specified
    print "File does not exist."
    result = None
    AWS_ACCESS_KEY = raw_input("Please enter AWS access key: ")
    AWS_SECRET_KEY = raw_input("Please enter AWS secret key: ")
    path_to_data = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/'
    path_to_fwf_file = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Python_Scripts/read_fwf.py'
    
    try:
        fullSchedule = af.s3_data_acquire(AWS_ACCESS_KEY, AWS_SECRET_KEY, path_to_data, path_to_fwf_file, qc_file_name = 'qc_streaming.csv')
    
    except IOError: #is this the right error if s3_data_acquire fails?
        print('Could not access streaming data!')
        quit()

#Get time window size
windows = af.sys.argv[2]
if windows is None:
    windows = 1800

#Determine broken run number, or get list of unhandled requests.
broken_Run = af.sys.argv[3]
if broken_Run is None:
    broken_Run = input("Please enter broken bus ID number as a string, OR, input a list of unhandled BookingIds: ")
if type(broken_Run) == str:
    case = 'BROKEN_RUN'
else:
    case = 'INDIVIDUAL_REQUESTS'
    individual_requests = broken_Run

resched_init_time = af.sys.argv[4]
if resched_init_time is None:
    try:
        resched_init_time = af.humanToSeconds(af.sys.argv[4])
    except:
        resched_init_time = af.humanToSeconds(raw_input('Enter a 24h time in HH:MM format\nfor initial time when buses can be rescheduled: '))

path_to_outdir = af.sys.argv[5]
if not af.os.path.isdir(path_to_outdir):
    print(path_to_outdir + ' is not a directory. Making that directory now...')
    af.os.mkdir(path_to_outdir)

# this simply returns full schedule with time windows at the moment
sched_obj = af.aTWC.TimeWindowsCapacity(fullSchedule)
fullSchedule_windows = sched_obj.addtoRun_TimeCapacity(1800.)
fS_w_copy = fullSchedule_windows.copy()
if type(fS_w_copy.index[0]) != int:
    fS_w_copy.index = range(0, fS_w_copy.shape[0])

# this gets us all the URIDs for the broken run given the initial rescheduling time
# OR it will get us URIDs given specific bookingIds to be rescheduled
if case == 'BROKEN_RUN':
    URIDs = af.get_URID_Bus(fullSchedule_windows, broken_Run, resched_init_time)
else:
    URIDs = af.get_URID_BookingIds(individual_requests)

# for each URID we find the bus runs to check through a radius elimination.
# for each URID for each run we then want to check the capacity in the given time
# window and return the URID with updated insert points. This URID with updated
# insert points is fed to the feasibilty function, which we ultimately want to return
# a minimum cost run for the URID and that run updated with the new URID slotted in.
taxi_costs = []
delay_costs = []
best_buses = []
for i in range(len(URIDs)):
    print('Rescheduling URID {0}'.format(i))
    busRuns_tocheck = af.radius_Elimination(fullSchedule_windows, URIDs[i], radius=4.)
    insert_stats = []
    for run in busRuns_tocheck:
        URID_updated_insertpts = af.checkCap.checkCapacityInsertPts(URIDs[i],run)
        runSchedule = af.get_busRuns(fullSchedule_windows, run, None)
        print('Testing feasibility for run ' + run)
        brokenwindows_dict =af.insertFeasibility(runSchedule, URID_updated_insertpts)
        if not brokenwindows_dict:
            print('Run {0} infeasible without moving the Activity 16 row.'.format(run))
        else:
            insert_stats.append(brokenwindows_dict)

    #ORDER buses by lowest additional lag time, i.e. total_lag, and sequentially add total_lag's
    ordered_inserts = sorted(insert_stats, key = af.operator.itemgetter('total_lag'))
    delay_costs.append(ordered_inserts[0]['total_lag'][0]*(48.09/3600)) #total dollars
    best_buses.append(ordered_inserts[0]['RunID'])

    #CALCULATE taxi cost
    taxi_costs.append(af.taxi(URIDs[i].PickUpCoords.LAT, URIDs[i].PickUpCoords.LON,
        URIDs[i].DropOffCoords.LAT, URIDs[i].DropOffCoords.LON, af.wheelchair_present(URIDs[i])))

    #WRITE information about best insertions to text file
    af.write_insert_data(URIDs[i], ordered_inserts[0:3],
        path_to_outdir, taxi_cost)
    
    #UPDATE whole day's schedule:
    fullSchedule_windows = af.day_schedule_Update(fullSchedule_windows, ordered_inserts[0], URIDs[i])
    
    #SAVE just the updated run for each URID
    fullSchedule_windows[fullSchedule_windows['Run'] == ordered_inserts[0]['RunID']].to_csv(af.os.path.join(path_to_outdir, str(str(int(URID.BookingId))+'_schedule.csv')), index = False)
    


#WRITE csv of PREFERRED OPTIONS:
if case == 'BROKEN_RUN':
    nrun_cost = af.newBusRun_cost(af.get_busRuns(fS_w_copy, broken_Run, URIDs[0]), provider = 6)
else:
    nrun_cost = None
pref_opt = af.preferred_options(URIDs, best_buses, delay_costs, taxi_costs, nrun_cost)
pref_opt.to_csv(af.os.path.join(path_to_outdir, 'preferred_costs.csv'), index = False)

#WRITE whole day's new schedule
if case == 'BROKEN_RUN':
    fullSchedule_windows = fullSchedule_windows[fullSchedule_windows['Run'] != broken_Run]

fullSchedule_windows.to_csv(af.os.path.join(path_to_outdir,'newSchedule.csv'), index = False)
    
