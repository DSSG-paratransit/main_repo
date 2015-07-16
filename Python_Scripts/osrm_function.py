import requests
import pandas as pd
import numpy as np

#osrm function
def osrm (URID_location, lats, lons):
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
    urid_LAT = str(URID_location[0]); urid_LON = str(URID_location[1])


        # outbound 
        for lat_cord,lon_cord in zip(lats[0:-1],lons[0:-1]): 
            out_route_url = out_osrm_url + "loc=" + urid_LAT + "," + urid_LON
            out_route_url = out_route_url+ "&loc=" + str(lat_cord) + "," + str(lon_cord) + "&instructions=false"
            out_route_requests = requests.get(out_route_url)
            out_route_results = out_route_requests.json()
            out_total_time += [out_route_results[u'route_summary'][u'total_time']]
            out_start_points += [out_route_results[u'route_summary'][u'start_point']]
            out_end_points += [out_route_results[u'route_summary'][u'end_point']]

        # inbound
        for lat_cord,lon_cord in zip(lats[1:],lons[1:]): 
            in_route_url = in_osrm_url + "loc=" + str(lat_cord) + "," + str(lon_cord) 
            in_route_url = in_route_url+ "&loc=" + urid_LAT + "," + urid_LON + "&instructions=false"
            in_route_requests = requests.get(in_route_url)
            in_route_results = in_route_requests.json()
            in_total_time += [in_route_results[u'route_summary'][u'total_time']]
            in_start_points += [in_route_results[u'route_summary'][u'start_point']]
            in_end_points += [in_route_results[u'route_summary'][u'end_point']]

    a = np.array([in_total_time]); b = np.array([out_total_time])
    ret = np.concatenate((a, b), axis = 0)
    total_route_df = pd.DataFrame(data = ret.T, columns=['inbound [1:]', 'outbound[0:-1]'])
    
    return(total_route_df)
