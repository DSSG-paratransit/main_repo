###Comparing ugly ride CPB to if they just took a taxi###

library(timeDate)
library(ggmap)

#Using northwest, $4.00 per mile
taxAm <- 4

#Get data set
data <- read.csv("QC4mo_and_cost.csv")
data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))
data$Run <- as.character(data$Run)

#Get ClientId and CPB from all ugly rides
ug_ind <- which(data$Ugly==1)
ug_clients <- data$ClientId[ug_ind]
ug_clients
ug_cpb <- data$ClientCost[ug_ind]
taxi_cost <- rep(0, length(ug_cpb))
cost_diff <- taxi_cost
ug_cost <- data.frame(ug_clients, ug_cpb, taxi_cost, cost_diff)

ug_cost <- cbind(ug_cost,)

#Don't need, just to look at
ug_run <- c(data$Run[ug_ind], data$ServiceDate[ug_ind])
routes <- data[which(data$Run == ug_run[1][[1]] & data$ServiceDate == ug_run[2][[1]]), ]

#need to get pickup and dropoff lat lons
#KIVAN: use the next line if you want to run the whole thing on the server
#for(i in 200:length(ug_ind))
for(i in 200:500){
  indx <- ug_ind[i]
  lats <- data$LAT[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  lons <- data$LON[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]

  #need to figure out distance from lat lon pair to another 
  #NOTE: python script must be in working directory, or should give path to it
  dist <- system(paste('python', 'mileage.py', lats[1], lons[1], lats[2], lons[2]), intern= T)
  dist <-  unlist(as.numeric(dist))
  
  #Osm output is in meters, so convert it to miles for cost
  distMi <- dist * 0.00062137119223733
  #cost is doubled because it goes to destination and back home
  taxiCost <- distMi * taxAm *2
  ug_cost$taxi_cost[i] <- taxiCost  
  ug_cost$cost_diff[i] <- ug_cost$ug_cpb[i]-ug_cost$taxi_cost[i]
}
  
#Get pickup lat,lon and dropoff lat,lon
#and then find taxi cost
#do the same for the ride home