#Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID
#

#Need to get data set to work with, probably want smaller to test on first
#Dataset needs to have the numPass and legTime columns added to it
#if not, check out AddLegTimes and PassengerCounts scripts
dataSet <- read.csv("UW_Trip_Data_FullCols.csv")

#Set the fixed bus cost per minute
#Average weighted bus cost is $48.09 per hour, so $0.8015 per minute
cost_per_minute <- .8015
#Creates array of all the different service days
ride_days = unique(dataSet$ServiceDate)
#Creates array of all the different client IDs
clients = unique(dataSet$ClientId)
clientCost <- NA
#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
costDF <- data.frame(1:8)
costDF <- t(costDF)
colnames(costDF) <- c("ClientCost", "ClientId", "Run", "ServiceDate", "LatStart",
                      "LonStart", "LatEnd", "LonEnd")



#clientCost <- numeric(length = nrow(clients))
for(k in 1:length(ride_days)){
  today = dataSet[which(dataSet$ServiceDate==ride_days[k]),]
  clients <- unique(today$ClientId)  
  #Clean for NAs because will always start with a NA client
  clients <- clients[which(!is.na(clients))]
  for(currentClient in 1:length(clients)){
    instances <- which(today$ClientId == clients[currentClient]) #gives rows of today that have clientID == currentClient
    if(length(instances) %% 2 == 0) {
      for(i in 1:(length(instances)/2)){
        instances[(i*2)-1]  #currentClient gets on
        clientRide = today[instances[(i*2)-1]:instances[i*2],]
        rideCost = 0
        for (j in 1:(length(clientRide)-1)){
          rideCost = rideCost + (clientRide$legTime[j]/clientRide$numPass[j])*cost_per_minute
        }
        #Put all the information from this run on this day for this client in the data frame
        costDF <- rbind(costDF, c(rideCost, clients[currentClient], clientRide$Run[1],
                        clientRide$ServiceDate[1], clientRide$LAT[1], clientRide$LON[1],
                        clientRide$LAT[length(clientRide)], clientRide$LON[length(clientRide)]))
        
      }
      
    }
    
  }
}


write.csv(costDF, 'CostDataFrame.csv')
