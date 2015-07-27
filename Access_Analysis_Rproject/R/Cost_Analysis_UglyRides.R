### Analysis of Ugly Rides ###

library(timeDate)
library(ggmap)


#Combine ride cost information with general routing data
setwd("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/")
dataToMerge <- read.csv("matchedMatrix.csv")
ugly_cost = quantile(dataToMerge$ClientCost, .9, na.rm= T)
dataToMerge$Ugly[which(dataToMerge$ClientCost <= ugly_cost)] <- 0
dataToMerge$Ugly[which(dataToMerge$ClientCost > ugly_cost)] <- 1
data <- cbind(format(read.csv("UW_Trip_Data_QC.csv"), digits = 9), dataToMerge[,2:4])

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




