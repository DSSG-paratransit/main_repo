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
    close_buses = radius_Elimination(dataTW, URID, resched_init_time, pickUpDropOff = True)

    for bus in close_buses:

        #Non-broken bus is currently at:
        bus_Run = get_busRuns(dataTW, bus, resched_init_time)
        #pd.data.frame of overlapping time windows:
        overlap_nodes = time_OL(bus_Run, URID, pickUpDropOff = True)

        plugLats = []; plugLons = [];

        #if there's a node before the first overlapping time window,
        #potentially insert URID between prior node and first node with overlapping TW.
        if overlap_nodes.index[0] != 0:
            plugLats.append(bus_Run.loc[overlap_nodes.index[0]-1].LAT)
            plugLons.append(bus_Run.loc[overlap_nodes.index[0]-1].LON)

        for kk in range(len(overlap_nodes.index)):
            plugLats.append(bus_Run.loc[overlap_nodes.index[0]].LAT)
            plugLons.append(bus_Run.loc[overlap_nodes.index[0]].LON)

        if overlap_nodes.index[len(overlap_nodes.index)] != 0:
            plugLats.append(bus_Run.loc[overlap_nodes.index[0]-1].LAT)
            plugLons.append(bus_Run.loc[overlap_nodes.index[0]-1].LON)

        D_table = kivansFunction(plugLats, plugLons, URID.PickUpCoords.tolist())

        #BEGIN TESTING POSSIBLE FITS OF URID ONTO BUS

        









