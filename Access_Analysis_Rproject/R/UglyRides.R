#Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID
#
library(timeDate)

dataSet <- read.csv("/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/UW_Trip_Data_QC.csv")
dataSet$ServiceDate <- as.timeDate(as.character(dataSet$ServiceDate))
cost_per_minute = 0.805

ride_days = unique(dataSet$ServiceDate)
#Creates array of all the different client IDs
clients = unique(dataSet$ClientId)
#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
costDF <- data.frame(1:8)
costDF <- t(costDF)
colnames(costDF) <- c("ClientCost", "ClientId", "Run", "ServiceDate", "LatStart",
                      "LonStart", "LatEnd", "LonEnd")
write.table(costDF, file = "./data/Cost_analysis.csv", col.names = T, sep = ",")



#clientCost <- numeric(length = nrow(clients))
for(k in 1:length(ride_days)){
  today = dataSet[which(dataSet$ServiceDate==ride_days[k]),]
  legTimes <- diff(today$ETA)
  today$legTimes <- c(legTimes, NA)
  clients <- na.omit(unique(today$ClientID))
  for(kk in 1:length(clients)){
    instances <- which(today$ClientID==clients[kk]) #gives rows of today that have clientID == currentClient
    if((length(instances) %% 2 == 0) & (length(instances) !=0)) {
      for(i in 1:(length(instances)/2)){
        instances[(i*2)-1] #currentClient gets on
        clientRide = today[instances[(i*2)-1]:instances[i*2],]
        rideCost = 0
        for (j in 1:(nrow(clientRide)-1)){
          rideCost = rideCost + (clientRide$legTimes[j]/clientRide$TotalPass[j])*(cost_per_minute/60)
        }
        
        newrow = data.frame(rideCost, clients[kk], clientRide$Run[1],
                             as.character(clientRide$ServiceDate[1]), clientRide$LAT[1], clientRide$LON[1],
                             clientRide$LAT[nrow(clientRide)], clientRide$LON[nrow(clientRide)])
        #Put all the information from this run on this day for this client in the data frame
        write.table(newrow, file = "./data/Cost_analysis.csv", col.names = F, append = T, sep = ",")
      }
    }
    if((length(instances) %% 2 != 0) & (length(instances) !=0)){
      sprintf("WARNING: number of clientID instances for %s on ride %s on day %s is %s", kk, clientRide$Run[1], ride_days[k], length(instances))}
  }
}



###########
# Open the cost analysis file and analyze CPB info
cost_data <- read.csv("data/Cost_analysis.csv", header = T)
upperCosts <- cost_data[which(cost_data$ClientCost != Inf & !is.na(cost_data$ClientCost)),]
CPB_sub <- upperCosts$ClientCost
hist(CPB_sub, breaks = seq(0, 500, 5)); abline(v = quantile(CPB_sub, 0.9), col = "red")
uglyrides <- upperCosts[which(CPB_sub>quantile(CPB_sub,0.9)),]
upperCosts <- upperCosts[which(upperCosts$ClientCost >quantile(CPB_sub, 0.9)), ]


##########
# Match the ugly rides with data in overall 4 month file



