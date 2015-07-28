#Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID
#
library(timeDate)

dataSet <- read.csv("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/UW_Trip_Data_QC.csv")
dataSet$ServiceDate <- as.timeDate(as.character(dataSet$ServiceDate))
dataSet$Run <- as.character(dataSet$Run) #get list of rides occuring on particular day
cost_per_sec = 0.805/60

ride_days = unique(dataSet$ServiceDate)
#Creates array of all the different client IDs
clients = unique(dataSet$ClientId)
#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
costDF <- data.frame(1:9)
costDF <- t(costDF)
colnames(costDF) <- c("ClientCost", "ClientId", "Run", "ServiceDate", "LatStart",
                      "LonStart", "LatEnd", "LonEnd", "AvgPass")
write.table(costDF, file = "./data/Cost_analysis.csv", col.names = T, sep = ",", row.names = F)


#clientCost <- numeric(length = nrow(clients))
for(k in 1:length(ride_days)){
  today = dataSet[which(dataSet$ServiceDate==ride_days[k]),]
  legTimes <- diff(today$ETA)
  today$legTimes <- c(legTimes, NA)
  today_rides <- unique(today$Run)
  for(kk in 1:length(today_rides)){
    #this_ride occuring on today
    this_ride <- today[which(today$Run == today_rides[kk]),]
    #clients on this_ride
    clients <- na.omit(unique(this_ride$ClientId))
    for (j in 1:length(clients)){
      #instances is one client's routing information
      instances <- which(this_ride$ClientId==clients[j]) #gives rows of today that have clientID == currentClient
      #print(length(instances))
      #analyze only on-boarding (not dropoff)
      if((length(instances) %% 2 == 0) & (length(instances) !=0)){
        for(jj in 1:(length(instances)/2)){
          PersonOnBus <- this_ride[(instances[(jj*2)-1]:instances[(jj*2)]),]
          rideCost = 0; avgPass = 0
          for (jjj in 1:(nrow(PersonOnBus)-1)){
            rideCost = rideCost + (PersonOnBus$legTimes[jjj]/PersonOnBus$NumPass[jjj])*(cost_per_sec)
            avgPass = avgPass + PersonOnBus$NumPass[jjj]
          }
          avgPass = avgPass/(nrow(PersonOnBus)-1)
          #save this ride cost
          newrow = data.frame(rideCost, clients[j], this_ride$Run[1],
                              as.character(this_ride$ServiceDate[1]), PersonOnBus$LAT[(jj*2)-1], PersonOnBus$LON[(jj*2)-1],
                              PersonOnBus$LAT[(jj*2)], PersonOnBus$LON[(jj*2)], avgPass)
          #Put all the information from this run on this day for this client in the data frame
          write.table(newrow, file = "/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/Cost_analysis.csv",
                      col.names = F, append = T, sep = ",", row.names = F)
        } 
      }
    }
  }
}

###########
# Open the cost analysis file and analyze CPB info. Be sure to reformat Cost_analysis.csv prior to loading (issue with row indices column)
cost_data <- read.csv("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/Cost_analysis.csv", header = T)
cost_data$ServiceDate <- as.timeDate(as.character(cost_data$ServiceDate))
cost_data <- cost_data[which(cost_data$ClientCost != Inf & !is.na(cost_data$ClientCost)),]
CPB_sub <- cost_data$ClientCost
hist(CPB_sub, breaks = seq(0, 500, 5), xlab = "Costs per boarding ($)", main = "CPB Distribution",
    xaxt = 'n', col = "cyan", ylab = "Number of boardings"); abline(v = quantile(CPB_sub, 0.9), col = "red")
axis(1, at = seq(0,500, 50))
uglyrides <- cost_data[which(CPB_sub>quantile(CPB_sub,0.9)),]
normalrides <- cost_data[which(CPB_sub<=quantile(CPB_sub,0.9)),]

##########
# Match the ugly rides with data in overall 4 month file
dataSet <- read.csv("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/UW_Trip_Data_QC.csv")
dataSet$ServiceDate <- as.timeDate(as.character(dataSet$ServiceDate))
dataSet$Run <- as.character(dataSet$Run)
cost_data$Ugly <- numeric(length = nrow(cost_data))
cost_data$Ugly[which(CPB_sub>quantile(CPB_sub,0.9))] <- 1

#search dataSub to match up ugly rides with comprehensive routing data:
dataSub <- dataSet
dataSub$Run <- as.character(dataSub$Run)
CostPassUg = matrix(NA, nrow = nrow(dataSub), ncol = 3)


#This loop takes 4ever...
for (kk in 1:nrow(cost_data)){
  ugly <- cost_data[kk,]
  ugCli <- which(dataSub$ServiceDate == ugly$ServiceDate & dataSub$Run == ugly$Run
                 & dataSub$ClientId== ugly$ClientId & dataSub$LAT == ugly$LatStart & dataSub$LON == ugly$LonStart)
  CostPassUg[ugCli,] <- c(ugly$ClientCost, ugly$AvgPass, ugly$Ugly)
}


###Ideas for ugly rides...
###check predominance of cities (heat map?)
###time of day, day of week prevelance?
