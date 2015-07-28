import requests
import pandas as pd
import numpy as np
from sys import argv

#Just to get the meters between two points
def mileage (lat1, lon1, lat2, lon2):
	osrm_url = "http://router.project-osrm.org/viaroute?"
	route_url = osrm_url+ "loc=" + str(lat1) + "," + str(lon1)
	route_url = route_url + "&loc=" + str(lat2) + "," + str(lon2) + "&instructions=false"
	#print route_url
	route_requests = requests.get(route_url)
	route_results = route_requests.json()
	#print route_results
	total_dist = route_results[u'route_summary'][u'total_distance']
	#print total_dist

	#print route_results.keys()
	return(total_dist)

# for testing
def main():	
	script, lat1, lon1, lat2, lon2 = argv
	print mileage(lat1, lon1, lat2, lon2)

if __name__ == "__main__":
	main()