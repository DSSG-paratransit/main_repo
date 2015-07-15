import requests
import pandas as pd
import numpy as np

data = pd.DataFrame.from_csv("../data/UW_Trip_Data_QC.csv")
lats = np.array(data.LAT[0:10]); lons = np.array(data.LON[0:10])

def dist_table_url(lats, lons):
    #lats and lons can be vectors, for multiple stop locations
    url = "http://router.project-osrm.org/viaroute?"
    for lat, lon in zip(lats, lons):
        url = url + "loc={" + str(lat) + "," + str(lon) + "}&"
    url = url + "instructions=false"
    n = len(lats)
    for ii in range(1,n):
        url += "&loc=%s,%s" % (str(lats[ii]), lons[ii])
    return(url)
        
def get_dist_table(url, n):
    #url of osrm api call, n is number of verticies
    out = requests.get(url)
    output = out.text.encode('ascii', 'ignore')
    mat = np.matrix(output[18:(len(output)-1)]).reshape([n,n])
    return(mat)
    
    
out = get_dist_table(dist_table_url(lats, lons), len(lats))
    
        
        
        
        
