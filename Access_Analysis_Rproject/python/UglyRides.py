import pandas as pd
import math

# Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID

# Need to get data set to work with, probably want smaller to test on first
# Dataset needs to have the numPass and legTime columns added to it
# if not, check out AddLegTimes and PassengerCounts scripts
dataSet = pd.read_csv("UW_Trip_Data_PassengerC.csv")

output = open('Cost_Data.csv', 'w')

# Set the fixed bus cost per minute
# Average weighted bus cost is $48.09 per hour, so $0.8015 per minute
cost_per_second = .8015/60

# need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
output.write("ClientCost,ClientId,Run,ServiceDate,LatStart,LonStart,LatEnd,LonEnd")

uniqueClientOB = dict()
currentDay = dataSet['ServiceDate'][1] 
currentRun = dataSet['Run'][1]
for i in dataSet.index:

	previousDay = currentDay
	previousRun = currentRun
	currentDay = dataSet['ServiceDate'][i]
	currentRun = dataSet['Run'][i]
	print(currentDay)

	clientID = dataSet['ClientId'][i]
	print(clientID)
  
	# create a new list of requests for a run
	if (currentRun != previousRun):
		uniqueClientOB = dict()
	if (currentDay != previousDay):
		uniqueClientOB = dict()
  	
  	# if no client for request row
  	if (math.isnan(clientID)):
  	  	print('ClientID is NA')
	# if start of client ride
  	elif clientID not in uniqueClientOB.keys():
   		uniqueClientOB[clientID] = [dataSet['ETA'][i], dataSet['LAT'][i], dataSet['LON'][i]]
  	# if end of client ride
  	else:
    	# commit data to csv, remove key from dictionary
   		startData = uniqueClientOB[clientID]
  	  	timeOnBus = dataSet['ETA'][i] - startData[0]
   		cost = timeOnBus * cost_per_second

		dataLine = "\n" + str(cost) + "," + str(clientID) + "," + str(currentRun) + "," +
					str(currentDay) + "," + str(startData[1]) + "," + str(startData[2]) +
					"," + str(dataSet['LAT'][i]) + "," + str(dataSet['LON'][i])
		print(dataLine)
		output.write(dataLine)
   		uniqueClientOB.pop(clientID, None)
