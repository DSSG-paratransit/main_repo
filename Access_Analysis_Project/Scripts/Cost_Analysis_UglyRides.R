### Analysis of Ugly Rides ###

#first half authored by Frank
#second half authored by Emily

library(timeDate)
library(ggmap)

#############Getting data the first time#########
#Combine ride cost information with general routing data
#setwd("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/")
#dataToMerge <- read.csv("matchedMatrix.csv")
#ugly_cost = quantile(dataToMerge$ClientCost, .9, na.rm= T)
#dataToMerge$Ugly[which(dataToMerge$ClientCost <= ugly_cost)] <- 0
#dataToMerge$Ugly[which(dataToMerge$ClientCost > ugly_cost)] <- 1
#data <- cbind(format(read.csv("UW_Trip_Data_QC.csv"), digits = 9), dataToMerge[,2:4])
#################################################

#This should be equivalent to commented block above
data <- read.csv("QC4mo_and_cost.csv")

data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))
data$Run <- as.character(data$Run)

########################## Plot routes containing ugly rides ##################################
# Pick a random run containing an ugly ride, plot it with ggmap
# good = 0
# while(good != 1){
#   #pick random route with an ugly ride.
#   dates = unique(data$ServiceDate)
#   rides = unique(data$Run)
#   rand_ug_ind <- sample(which(data$Ugly==1), 1)
#   rand_ug_run <- c(data$Run[rand_ug_ind], data$ServiceDate[rand_ug_ind])
#   route <- data[which(data$Run == rand_ug_run[1][[1]] & data$ServiceDate == rand_ug_run[2][[1]]), ]
#   if(any(c(20, 21, 22, 40, 41, 42, 43, 44, 45)%in%route$Activity)){
#     good = 0
#   }
#   else{good = 1}
# }
# 
# route$ClientId <- suppressWarnings(as.numeric(route$ClientId))
# clients_route <- na.omit(route$ClientId)
# for(cli in clients_route){
#   temp <- route[which(route$ClientId == cli),]
#   if(nrow(temp)%%2 != 0){stop("Client only mentioned once!")}
#   #take on-boarding CPB and make it the off-boarding CPB too, i.e. match CPB's for a client, for leg coloring purposes.
#   for(kk in seq(from = 2, to = nrow(temp), by =2)){
#     route[which(row.names(route)==row.names(temp[kk,])), c("ClientCost", "AvgPass", "Ugly")] <- temp[kk-1,c("ClientCost", "AvgPass", "Ugly")]
#   }
# }
# 
# #make all legs in between an ugly CPB ugly, to indicate on map:
# ctr = 1; ugVec <- matrix(0, nrow = nrow(route), ncol = 1)
# row.names(route) <- 1:nrow(route)
# for(cli in clients_route){
#   temp <- route[which(route$ClientId == cli),]
#   for(jj in 1:(nrow(temp)/2)){
#     if(temp$Ugly[(jj*2) - 1] == 1){
#       ugVec[row.names(temp)[(jj*2) - 1]:row.names(temp)[(jj*2)]] <- 1
#     }
#   }
# }
# 
# plotRoute <- route
# plotRoute$Ugly <- ugVec
# 
# lons = as.numeric(unlist(plotRoute$LON))
# lats = as.numeric(unlist(plotRoute$LAT))
# zm = 11
# 
# center_King_Co = c(quantile(lons,.5, type = 4), quantile(lats,.5, type = 4))
# map <- get_googlemap(center = center_King_Co, zoom = zm, maptype = "roadmap", messaging = FALSE)
# 
# p <- ggmap(map, extent = "device")+
#   geom_point(aes(x = lons, y = lats), data =plotRoute, size = sqrt(2), colour = "black")+
#   geom_segment(aes(x = lons[1], y = lats[1], xend = lons[2], yend = lats[2]), size = .24, colour = "green")
# 
# for (j in 2:(nrow(plotRoute)-1)){
#   if (plotRoute$Ugly[j]==0){
#     p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data=plotRoute, size = .24, colour = "green")
#   }
#   else{
#     p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data =plotRoute, size = .24, colour = "red")
#   }
# }
# 
# print(p)


######################## Randomly sample Bus Runs, see if it contains ugly ride ##############################

#number of simulations:
# N = 10000
# storUg <- matrix(NA, nrow = N, ncol = 1)
# data_rel <- data[,c("ServiceDate", "Run", "Ugly")]
# dates = unique(data$ServiceDate); dn = length(dates)
# rides = unique(data$Run); rn = length(rides)

# for(j in 1:N){
#   rand_date <- dates[sample(1:dn,1)]
#   rand_ride <- rides[sample(1:rn,1)]
#   route <- data_rel[which(data_rel$Run == rand_ride & data_rel$ServiceDate == rand_date), ]
#   if (any(na.omit(route$Ugly) == 1)){storUg[j] <- 1}
#   else{
#     storUg[j] <- 0}
#   print(j)
# }

######################## Count how many runs have ugly rides ##############################
data_rel <- data[,c("ServiceDate", "Run", "Ugly", "City")]
storMat <- matrix(NA, nrow = 1, ncol = 4)
colnames(storMat) <- colnames(data_rel)
dates = unique(data$ServiceDate); dn = length(dates)
for(j in 1:dn){
  day = data_rel[data_rel$ServiceDate == dates[j],]
  day_rides = unique(day$Run)
  for(k in 1:length(day_rides)){
    this_run = day[day$Run==day_rides[k],]
    if (any(this_run$Ugly ==1, na.rm = T)){
      #add
      storMat <- rbind(storMat, matrix(c(this_run$ServiceDate, this_run$Run, 1, )))
    }
    else{
      ugYN <- c(ugYN, 0)
    }
  }
}

ugRidePrevalence = 100*sum(ugYN)/length(ugYN)



#########################Comparing ugly ride CPB to if they just took a taxi######################################
#Ask Emily with questions about code after here

#Using northwest, $4.00 per mile (most expensive ambulatory taxi)
#This could be made more accurate by using diff taxi costs, see travelCosts.py for ideas
taxAm <- 4


#Get ClientId and CPB from all ugly rides, and make new dataframe called ug_cost
ug_ind <- which(data$Ugly==1)
ug_clients <- data$ClientId[ug_ind]
ug_cpb <- data$ClientCost[ug_ind]
taxi_cost <- rep(0, length(ug_cpb))
cost_diff <- taxi_cost
ug_cost <- data.frame(ug_clients, ug_cpb, taxi_cost, cost_diff)


#Go through ugly rides and find the cost for using a taxi instead
for(i in 1:length(ug_ind)){
  indx <- ug_ind[i]
  #need to get pickup and dropoff lat lons
  #currently just finds first pickup and first dropoff, and doubles that, assuming client only
  #goes to one location and then back home, 
  #another more thorough version can be found in the next section, this is preferable
  #when you need fas
  lats <- data$LAT[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  lons <- data$LON[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  
  #need to figure out distance from lat lon pair to another 
  #NOTE: python script must be in working directory, or should give path to it
  dist <- system(paste('python', 'mileage1.py', lats[1], lons[1], lats[2], lons[2]), intern= T)
  dist <-  unlist(as.numeric(dist))
  
  #Osm output is in meters, so convert it to miles for cost
  distMi <- dist * 0.00062137119223733
  #cost is doubled because it goes to destination and back home
  taxiCost <- distMi * taxAm *2
  ug_cost$taxi_cost[i] <- taxiCost  
  ug_cost$cost_diff[i] <- ug_cost$ug_cpb[i]-ug_cost$taxi_cost[i]
}


miles <- ug_done$taxi_cost/taxAm/2 
ug_cost <- cbind(ug_cost, miles)
##################### Some prelim analysis #####################

meanDiff <- mean(ug_cost$cost_diff)
maxDiff <- max(ug_cost$cost_diff)
ug_cost <- ug_cost[with(ug_cost, order(-cost_diff)), ]
ug_better <- ug_cost[which(ug_cost$cost_diff>0),]
#3429 out of 28105 would have been better off on taxis, most savings $461.80
#only 12.2% of ugly rides would be better on taxi
weird <- ug_cost[which(ug_cost$taxi_cost==0),]

pickupTime1 <- rep(0, length(ug_cpb))
pickupTime2 <- pickupTime1
dropoffTime1 <-pickupTime1
dropoffTime2 <- pickupTime1
numStops <- rep(0, length(ug_cpb))
dates <- rep(0, length(ug_cpb))

for(i in 1:length(ug_cost$ug_cpb)){
  indx <- ug_ind[i]
  #times <- data$ETA[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  #lats <- data$LAT[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  #lons <- data$LON[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  dates[i] <- as.character(data$ServiceDate[indx])
  #numStops[i] <- length(lats)
  #pickupTime1[i] <- times[1]
  #pickupTime2[i] <-times[2]
  #dropoffTime1[i] <- times[length(times)-1]
  #dropoffTime2[i] <-times[length(times)]
  
}

ug_cost <- cbind(ug_cost, dates) #, numStops, pickupTime1, pickupTime2, dropoffTime1, dropoffTime2)

###################Fixing weird costs (specifically zeros)###############
weird <- ug_cost[which(ug_cost$taxi_cost==0),]
badSched <- rep(0, length(weird$ug_clients))
weird <- cbind(weird, badSched)
for (i in 1:length(weird$ug_clients))
{
  
  weirdRows <- data[which(as.integer(as.character(data$ClientId)) == weird$ug_clients[i] & as.character(data$ServiceDate) == weird$dates[i]), ]
  if(max(weirdRows$SchedStatus)>=20)
  {
    weird$badSched[i] <- 1
  }
}

weird <- weird[which(weird$badSched==0),]
#returning nothing, not sure why
data[which(data$ClientId == weird$ug_clients[1] & as.character(data$ServiceDate) == weird$dates[1]), ]
test <- data[which(data$ClientCost==weird$ug_cpb[1]),]

as.character(test$ServiceDate) == weird$dates[1]


#################################Trying to correct zeros only ########################################
for(i in 1:length(ug_ind)){
  indx <- ug_ind[i]
  lats <- data$LAT[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  lons <- data$LON[which(data$ClientId == data$ClientId[indx] & data$ServiceDate == data$ServiceDate[indx])]
  #only call osrm for $0 taxi rides
  if (ug_cost$taxi_cost[i]==0){
    #check through all lat, lon pairs to find total distMi
    for(i in 1:length(lats)-1){
      #when the location doesn't change
      if(lats[i]==lats[i+1] && lons[i]==lons[i+1])
      {
        #get rid of one of the locations
        lats <- lats[-i]
        lons <- lons[-i]
      }
      else{
        dist <- system(paste('python', 'mileage1.py', lats[i], lons[i], lats[i+1], lons[i+1]), intern= T)
        dist <-  unlist(as.numeric(dist))
        
        #Osm output is in meters, so convert it to miles for cost
        distMi <- distMi + (dist * 0.00062137119223733)
      }
    }
    
  } 
  #with 18mo want to use wheelchair if statement to get more accurate cost
  taxiCost <- distMi * taxAm 
  ug_cost$taxi_cost[i] <- taxiCost  
  ug_cost$cost_diff[i] <- ug_cost$ug_cpb[i]-ug_cost$taxi_cost[i]
}
########################Combining taxi costs with full data #################################
ug_cost <- read.csv("./ugly_rides_cost_compare.csv")
full_data <- read.csv("./QC4mo_and_cost.csv")
full_data$ServiceDate <- as.timeDate(as.character(full_data$ServiceDate))
ug_cost$ServiceDate <- as.timeDate(as.character(ug_cost$dates))


#add TaxiCost and CostDiff column to full_data
TaxiCost <- rep(0, length(full_data$X))
CostDiff <- TaxiCost
full_data <- cbind(full_data, TaxiCost, CostDiff)

for(i in 1:length(ug_cost$ug_clients))
{
  indx <- which(as.character(full_data$ServiceDate)==paste(c(as.character("00"),as.character(ug_cost$dates[1])), collapse="") && full_data$ClientId==ug_cost$ug_clients[i] && full_data$ClientCost==ug_cost$ug_cpb[i])
  full_data$TaxiCost[indx] <- ug_cost$taxi_cost[i]
  full_data$CostDiff[indx] <- ug_cost$cost_diff[i]
}

######################save the df that has the cost comparison###############################
write.table(x = ug_cost, file = "./data/ugly_rides_cost_compare.csv", sep = ",")
write.table(x = full_data, file = "./data/ugly_rides_Tableau.csv", sep = ",")

ug_cost <- read.csv("./ugly_rides_cost_compare.csv")




