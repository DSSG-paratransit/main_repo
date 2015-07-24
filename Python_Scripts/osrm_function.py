import requests
import pandas as pd
import numpy as np

#osrm function
def osrm (URID_location, busRun):
    #URID_location it's a lat, lon list of URID 
    #lists for inbound and outbound matrices
    # outbound (from urid location to scheduled location)
    # and inbound (from scheduled location to urid location) 
    out_total_time = []
    out_start_points = []
    out_end_points = []
    in_total_time = []
    in_start_points = []
    in_end_points = []
    out_osrm_url = "http://router.project-osrm.org/viaroute?"
    in_osrm_url = "http://router.project-osrm.org/viaroute?"

        # outbound 
        for lat_cord,lon_cord in zip(subset.LAT,subset.LON): 
            out_route_url = out_osrm_url + "loc=" + str(urid.LAT) + "," + str(urid.LON) 
            n = len(subset.LAT)
            out_route_url = out_route_url+ "&loc=" + str(lat_cord) + "," + str(lon_cord) + "&instructions=false"
            out_route_requests = requests.get(out_route_url)
            out_route_results = out_route_requests.json()
            out_total_time += [out_route_results[u'route_summary'][u'total_time']]
            out_start_points += [out_route_results[u'route_summary'][u'start_point']]
            out_end_points += [out_route_results[u'route_summary'][u'end_point']]

        # inbound
        for lat_cord,lon_cord in zip(subset.LAT,subset.LON): 
            in_route_url = in_osrm_url + "loc=" + str(lat_cord) + "," + str(lon_cord) 
            n = len(subset.LAT)
            in_route_url = in_route_url+ "&loc=" + str(urid.LAT) + "," + str(urid.LON) + "&instructions=false"
            in_route_requests = requests.get(in_route_url)
            in_route_results = in_route_requests.json()
            in_total_time += [in_route_results[u'route_summary'][u'total_time']]
            in_start_points += [in_route_results[u'route_summary'][u'start_point']]
            in_end_points += [in_route_results[u'route_summary'][u'end_point']]

    out_bus_matrix = (out_end_points, out_total_time)
    in_bus_matrix = (in_end_points, in_total_time)

    total_bus_matrix = {'outbound_location':out_bus_matrix[0],'outbound_time':out_bus_matrix[1],'inbound_location':in_bus_matrix[0],'inbound_time':in_bus_matrix[1]}
    total_route_df = pd.DataFrame(data=total_bus_matrix)
    #print(total_route_df)
