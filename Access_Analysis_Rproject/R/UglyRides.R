#Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID
#

#Need to get data set to work with, probably want smaller to test on first

#Set the fixed bus cost per minute
#Average weighted bus cost is $48.09 per hour, so $0.8015 per minute
cost_per_minute <- .8015
#Creates array of all the different service days
 ride_days = unique(AD_56$ServiceDate)
 #Creates array of all the different client IDs
 clients = unique(ride_days$ClientId)
 clientCost <- numeric(length = nrow(clients))
 for(k in 1:length(ride_days)){ 
    today = AD_56[which(AD_56$ServiceDate==ride_days[k]),]
    for(currentClient in 1:length(clients)){
      clientRide <- AD_56[which(AD_56$ClientId == clients[currentClient])]
      for (j in 1:length(clientRide)){
        legCost <- (clientRide$legTime[j]/clientRide$numPass[j])*cost_per_minute
        clientCost[currentClient] <- clientCost[currentClient] + legCost
    
      }
    }
 }
 
 #Appends the client cost as new column to clients
 clients$clientCost <- clientCost
 #To find ugly rides we'll want to to look at clients df
