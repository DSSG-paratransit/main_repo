import requests
import pandas as pd
import numpy as np

#Get distances between (insertable nodes, URID location)
def osrm (URID_location, inbound, outbound):
    #URID_location it's a list: [lat, lon]
    #lists for inbound and outbound matrices
    # inbound/outbound: 2-column np.arrays storing inbound/outbound node latitude/longitude
    # and inbound (from scheduled location to urid location) 
    total_times = []
    out_start_points = []
    out_end_points = []
    in_total_time = []
    in_start_points = []
    in_end_points = []
    osrm_url = "http://router.project-osrm.org/viaroute?"
    urid_LAT = URID_location[0]; urid_LON = URID_location[1]

    # outbound
    for k in outbound.shape[0]: 
        lat_cord_O = outbound[k, 0]; lon_cord_O = outbound[k, 1]
        lat_cord_I = inbound[k, 0]; lon_cord_I = inbound[k, 1]
        
        route_url = osrm_url+ "loc=" + str(lat_cord_O) + "," + str(lon_cord_O)
                         + "&loc=" + str(urid_LAT) + "," + str(urid_LON) + "&loc=" + str(lat_cord_I) + "," + str(lon_cord_I) +
                         "&instructions=false"
        
        route_requests = requests.get(route_url)
        route_results = route_requests.json()
        total_times += [route_results[u'route_summary'][u'total_time']]

    a = np.array([total_times])
    
    return(a.T)



#IMPLEMENTATION:
#formulate URID's location:4
# if pickUpDropOff:
#     URID_loc = ([URID.PickUpCoords["LAT"], URID.PickUpCoords["LON"]])
# else:
#     URID_loc = ([URID.DropOffCoords["LAT"], URID.PickUpCoords["LON"]])

#formulate inbound nodes and outbound nodes, for input into OSRM!!!
# inserts = time_overlap(Run_Schedule, URID, pickUpDropOff)
# outbound = Run_Schedule.loc[inserts["outbound"]]
# outbound = np.column_stack((np.array(outbound.LAT), np.array(outbound.LON)))
# inbound = Run_Schedule.loc[inserts["inbound"]]
# inbound = np.column_stack((np.array(inbound.LAT), np.array(inbound.LON))) 

# time_matrix = osrm(uridLoc, inbound, outbound)

#We now have travel times for the inbound, outbound insertions!
# time_matrix["inbound_times"]; time_matrix["outbound_times"]
# outbound = np.column_stack((outbound, time_matrix["outbound_times"].T))
# inbound = np.column_stack((inbound, time_matrix["inbound_times"].T))
# outbound
