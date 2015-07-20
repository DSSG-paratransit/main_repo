#### Psuedo code for MAIN file for Access rerouting #####
import pandas as pd
import numpy as np
import haversine from haversine

#Path to cleaned up data for the day:
clean_data_path = '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/single_clean_day.csv'

broken_Run = '680SEB' #RunID
resched_init_time = 13*60 + 30 # 1:30 PM (in sec). Initial time IN SECONDS that we will begin rerouting buses.
data = pd.read_csv(clean_data_path, header = True) #import one day's QC'ed data
windowsz = 30*60#Variable window size

dataTW = add_TimeWindows(data, windowsz)

URIDS = get_URIDs(dataTW, broken_Run, resched_init_time)

for URID in URIDS:
    #CHECK PICK-UP INSERTIONS:
    #list of nearby buses within URID's time frame:
    radius = 5
    good_buses = radius_Elimination(dataTW, URID, radius, pickUpDropOff = True)

    for bus in good_buses:

        #Non-broken bus is currently at:
        bus_Run = get_busRuns(dataTW, bus, resched_init_time)
        #get inbound overlap nodes and outbound overlap nodes...
        overlap_nodes = time_overlap(bus_Run, URID, pickUpDropOff = True)

        #formulate inbound nodes and outbound nodes, for input into OSRM!!!
        outbound = Run_Schedule.loc[overlap_nodes["outbound"]]
        outbound = np.column_stack((np.array(outbound.LAT), np.array(outbound.LON)))
        inbound = Run_Schedule.loc[overlap_nodes["inbound"]]
        inbound = np.column_stack((np.array(inbound.LAT), np.array(inbound.LON)))

        #get URID's pickup location:
        uridLoc = [URID.PickUpCoords[0], URID.PickUpCoords[1]]

        #get matrix of times between URID and scheduled route's nodes...
        time_matrix = osrm(uridLoc, inbound, outbound)

        #We now have travel times for the inbound, outbound insertions!
        outbound_times = np.column_stack((outbound, time_matrix["outbound_times"].T))
        inbound_times = np.column_stack((inbound, time_matrix["inbound_times"].T)) 

        
        

        #BEGIN TESTING POSSIBLE FITS OF URID ONTO BUS


        









