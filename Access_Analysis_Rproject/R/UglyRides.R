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
# dataSet <- read.csv("UW_Trip_Data.csv")

#Set the fixed bus cost per minute
#Average weighted bus cost is $48.09 per hour, so $0.8015 per minute
cost_per_second <- .8015/60

#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
write.table(t(c("ClientCost", "ClientId", "Run", "ServiceDate", "LatStart",
                "LonStart", "LatEnd", "LonEnd")),file='Cost_Data.csv',col.names=F,
            row.names=F,sep=',')

uniqueClientOB = list()
currentDay = dataSet$ServiceDate[1] 
currentRun = dataSet$Run[1]
for (i in 1:nrow(dataSet)) {
  previousDay = currentDay
  previousRun = currentRun
  currentDay = dataSet$ServiceDate[i]
  currentRun = dataSet$Run[i]
  print(currentDay)
  
  clientID = as.character(dataSet$ClientId[i])
  print(clientID)
  
  if (currentRun != previousRun) {
    uniqueClientOB = list()
  }
  if (currentDay != previousDay) {
    uniqueClientOB = list()
  }
  
  if (is.na(clientID)) {
    print('ClientID is NA')
  } else if (is.null(uniqueClientOB[[clientID]])) {
    uniqueClientOB[[clientID]] <- c(dataSet$ETA[i], dataSet$LAT[i],
                                    dataSet$LON[i])
  } else {
    # commit to datafame, remove key from list
    startData = uniqueClientOB[[clientID]]
    timeOnBus = dataSet$ETA[i] - startData[1]
    cost = timeOnBus * cost_per_second
    dataLine = c(cost,clientID,as.character(currentRun),as.character(currentDay)
                 ,startData[2],startData[3],dataSet$LAT[i],dataSet$LON[i])
    print(dataLine)
    write.table(t(dataLine),file="Cost_Data.csv",append=T,col.names=F,row.names=F,
                sep=',')
    uniqueClientOB[[clientID]] <- NULL
  }
  
}


# will this help merge in git?













