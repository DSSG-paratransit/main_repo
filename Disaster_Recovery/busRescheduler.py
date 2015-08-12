import all_functions as af


def busReschedule_run(schedule_filename, accesskey, secretkey, bookingid, broken_run, windows = 1800.,resched_init_time = None, path_to_outdir = af.os.join.path(af.os.getcwd(),'data'), radius = 3.):

  '''
      schedule_filename (str): name of file to be used if you want to test a DEMO file. Must be a single day, QC'ed file.
      accesskey (str): AWS_ACCESS_KEY
      secretkey (str): AWS_SECRET_KEY
      bookingid (?): list of BookingIds to be rescheduled (comma separated?)
      broken_run (str): name of broken run.
      windows (float): size of time windows, in seconds
      resched_init_time (int): seconds in day at which rescheduling can occur.
      path_to_outdir (str): path to directory where you would like to store all output files.
      radius (float): number of miles to search for close buses. Will be shrunk by increments of 1 if
                      number of nearby buses is > 30.

      '''
    flag = 400 #400 is good, 200 is bad.

    #get data
    if schedule_filename is not None:
        if af.os.path.isfile(schedule_filename):
            fullSchedule = af.pd.DataFrame.from_csv(schedule_filename, header=0, sep=',')

    else:
        #grab s3 streaming_data/ file if no file specified
        print "File does not exist."

    if accesskey and secretkey is not None:
        AWS_ACCESS_KEY = raw_input("Please enter AWS access key: ")
        AWS_SECRET_KEY = raw_input("Please enter AWS secret key: ")
        if not af.os.path.exists(path_to_outdir):
            path_to_outdir = af.os.join.path(af.os.getcwd(),'data')

        try:
            fullSchedule = af.s3_data_acquire(accesskey, secretkey, path_to_outdir, qc_file_name = 'qc_streaming.csv')
            if fullSchedule == -1:
              flag = 200
              return flag

        except IOError: #is this the right error if s3_data_acquire fails?
            print('Could not access streaming data!')
            flag = 200
            return flag
        except:
            print('Other error in acquiring streaming_data.')
            flag = 200
            return flag
            
    #Determine broken run number, or get list of unhandled requests.
    if broken_run is not None:
        case = 'BROKEN_RUN'
    elif bookingid is not None:
        case = 'INDIVIDUAL_REQUESTS'
        individual_requests = list(bookingid)

    # this simply returns full schedule with time windows at the moment
    sched_obj = af.aTWC.TimeWindowsCapacity(fullSchedule)
    fullSchedule_windows = sched_obj.addtoRun_TimeCapacity(windows)
    fS_w_copy = fullSchedule_windows.copy()

    #this gets us all the URIDs for the broken run given the initial rescheduling time
    #OR it will get us URIDs given specific bookingIds to be rescheduled
    if case == 'BROKEN_RUN':
        if broken_run not in list(set(fullSchedule_windows.Run.tolist())):
            print('Run number is not scheduled for today!')
            flag = 200
            return flag

        if resched_init_time is None:
            resched_init_time = af.humanToSeconds(raw_input('Enter a 24h time in HH:MM format\nfor initial time when buses can be rescheduled: '))

        URIDs = af.get_URID_Bus(fullSchedule_windows, broken_run, resched_init_time) 

    else:
        for i in range(len(individual_requests)):
            if individual_requests[i] not in list(set(fullSchedule_windows.BookingId.tolist())):
                print('You have entered BookingIds not present in the schedule!')
                flag = 200
                return flag

        URIDs = af.get_URID_BookingIds(fullSchedule_windows, individual_requests)

    if not URIDs:
        print('There are no people to reschedule on bus {0} at time {1}'.format(broken_run, resched_init_time))
        flag = 200
        return flag

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
        busRuns_tocheck = af.radius_Elimination(fullSchedule_windows, URIDs[i], radius=radius)
        insert_stats = []

        #iterate over all runs, find best one!
        for run in busRuns_tocheck:

            this_run = fullSchedule_windows[fullSchedule_windows['Run']==run]
            capacity_obj = af.checkCap.CapacityInsertPts(this_run)

            #Kristen's capacity checker:
            URIDs[i].PickupInsert, URIDs[i].DropoffInsert = capacity_obj.return_inserts(URIDs[i])

            # IF THERE'S ROOM: TEST FEASIBILITY
            if not af.np.isnan(URIDs[i].PickupInsert):
                URIDs[i].PickupStart = URIDs[i].PickupInsert
                URIDs[i].DropoffStart = URIDs[i].DropoffInsert

                runSchedule = af.get_busRuns(fullSchedule_windows, run, None)
                print('Testing feasibility for run ' + run)
                brokenwindows_dict =af.insertFeasibility(runSchedule, URIDs[i])
                if not brokenwindows_dict:
                    print('Run {0} infeasible without moving the return-to-garage row.'.format(run))
                else:
                    insert_stats.append(brokenwindows_dict)

        #ASSEMBLE and ORDER transit options.
        if insert_stats:
            #ORDER buses by lowest additional lag time, i.e. total_lag, and sequentially add total_lag's
            ordered_inserts = sorted(insert_stats, key = af.operator.itemgetter('total_lag'))
        
            popme = []
            for k in range(len(ordered_inserts)):
                if ordered_inserts[k]['RunID']==broken_run:
                    popme.append(k)
            if popme:
                ordered_inserts.pop(popme)


            delay_costs.append(ordered_inserts[0]['total_lag'][0]*(48.09/3600)) #total dollars
            best_buses.append(ordered_inserts[0]['RunID'])

            #CALCULATE taxi cost
            taxi_costs.append(af.taxi(URIDs[i].PickUpCoords[0], URIDs[i].PickUpCoords[1],
                URIDs[i].DropOffCoords[0], URIDs[i].DropOffCoords[1], af.wheelchair_present(URIDs[i])))

            #WRITE information about best insertions to text file
            af.write_insert_data(URIDs[i], ordered_inserts[0:3],
                path_to_outdir, taxi_costs[i])

            #UPDATE whole day's schedule:
            fullSchedule_windows = af.day_schedule_Update(data = fullSchedule_windows, top_Feasibility = ordered_inserts[0], URID = URIDs[i])
            sched_obj_update = af.aTWC.TimeWindowsCapacity(fullSchedule_windows)
            fullSchedule_windows = sched_obj_update.add_Capacity(update = True)

            #SAVE just the updated run for each URID
            fullSchedule_windows[fullSchedule_windows['Run'] == ordered_inserts[0]['RunID']].to_csv(af.os.path.join(path_to_outdir, str(str(int(URIDs[i].BookingId))+'_schedule.csv')), index = False)

        else:
            delay_costs.append(400000)
            taxi_costs.append(af.taxi(URIDs[i].PickUpCoords[0], URIDs[i].PickUpCoords[1],
                URIDs[i].DropOffCoords[0], URIDs[i].DropOffCoords[1], af.wheelchair_present(URIDs[i])))
            best_buses.append('NA')

    #WRITE csv of PREFERRED OPTIONS:
    if case == 'BROKEN_RUN':
        nrun_cost = af.newBusRun_cost(af.get_busRuns(fS_w_copy, broken_run, URIDs[0]), provider = 6)
    else:
        nrun_cost = None
    pref_opt = af.preferred_options(URIDs, best_buses, delay_costs, taxi_costs, nrun_cost)
    pref_opt.to_csv(af.os.path.join(path_to_outdir, 'preferred_options.csv'), index = False)

    return flag
