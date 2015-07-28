import requests
import pandas as pd
import numpy as np
from sys import argv

'''
@params: takes two lat/lon pairs (start and end points)
@returns: the total street network distance between the pairs
'''
def mileage (lat1, lon1, lat2, lon2):
	route_results = getOSRMOutput(lat1, lon1, lat2, lon2)
	total_dist = route_results[u'route_summary'][u'total_distance']
	#print total_dist
	return(total_dist)

'''
@params: takes two lat/lon pairs (start and end points)
@returns: the total non traffic time it would take to get between the two pairs
'''
def time (lat1, lon1, lat2, lon2):
	route_results = getOSRMOutput(lat1, lon1, lat2, lon2)
	total_time = route_results[u'route_summary'][u'total_time']
	# print total_time
	return(total_time)

'''
@params: takes two lat/lon pairs (start and end points)
@returns: a json object containing data about traveling between the two pairs
'''
def getOSRMOutput (lat1, lon1, lat2, lon2):
	osrm_url = "http://router.project-osrm.org/viaroute?"
	route_url = osrm_url+ "loc=" + str(lat1) + "," + str(lon1)
	route_url = route_url + "&loc=" + str(lat2) + "," + str(lon2) + "&instructions=false"
	#print route_url
	route_requests = requests.get(route_url)
	route_results = route_requests.json()
	#print route_results
	return route_results

# for testing
def main():	
	script, lat1, lon1, lat2, lon2 = argv
	print mileage(lat1, lon1, lat2, lon2)
	print time(lat1, lon1, lat2, lon2)

if __name__ == "__main__":
	main()