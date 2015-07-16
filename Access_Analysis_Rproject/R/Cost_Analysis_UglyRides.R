### Analysis of Ugly Rides ###

#Combine ride cost information with general routing data
setwd("/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/")
dataToMerge <- read.csv("matchedMatrix.csv")
data <- cbind(format(read.csv("UW_Trip_Data_QC.csv"), digits = 9), dataToMerge[,2:4])


library(timeDate)
library(ggmap)

data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))
data$Run <- as.character(data$Run)

good = 0
while(good != 1){
  #pick random route with an ugly ride.
  dates = unique(data$ServiceDate)
  rides = unique(data$Run)
  rand_ug_ind <- sample(which(data$Ugly==1), 1)
  rand_ug_run <- c(data$Run[rand_ug_ind], data$ServiceDate[rand_ug_ind])
  route <- data[which(data$Run == rand_ug_run[1][[1]] & data$ServiceDate == rand_ug_run[2][[1]]), ]
  if(any(c(20, 21, 22, 40, 41, 42, 43, 44, 45)%in%route$Activity)){
    good = 0
  }
  else{good = 1}
}

clients_route <- na.omit(unique(route$ClientId))
for(cli in clients_route){
  temp <- route[which(route$ClientId == cli),]
  if(nrow(temp)%%2 != 0){stop("Client only mentioned once!")}
  #take on-boarding CPB and make it the off-boarding CPB too, i.e. match CPB's for a client, for leg coloring purposes.
  for(kk in seq(from = 2, to = nrow(temp), by =2)){
    route[which(row.names(route)==row.names(temp[kk,])), c("ClientCost", "AvgPass", "Ugly")] <- temp[kk-1,c("ClientCost", "AvgPass", "Ugly")]
  }
}

#make all legs in between an ugly CPB ugly, to indicate on map:
ctr = 1; ugVec <- matrix(0, nrow = nrow(route), ncol = 1)
row.names(route) <- 1:nrow(route)
for(cli in clients_route){
  temp <- route[which(route$ClientId == cli),]
  if(nrow(temp)==2){
    if(temp$Ugly[1] == 1){
    ugVec[row.names(temp)[1]:row.names(temp)[2]] <- 1
    }
  }
  else{print("RUN AGAIN")}
}
plotRoute <- route
plotRoute$Ugly <- ugVec


lons = as.numeric(plotRoute$LON)
lats = as.numeric(plotRoute$LAT)
zm = 10

center_King_Co = c(mean(lons), mean(lats))
map <- get_googlemap(center = center_King_Co, zoom = zm, maptype = "roadmap")

p <- ggmap(map)+
  geom_point(aes(x = lons, y = lats), data = as.numeric(plotRoute[,c("LAT", "LON")]), size = sqrt(2), colour = "black")+
  geom_segment(aes(x = lons[1], y = lats[1], xend = lons[2], yend = lats[2]), data = temp, size = .24, colour = "red")
if(nrow(pl))
for (j in 1:nrow()){
  if (plotRoute$Ugly[j]==0){
    p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data=as.numeric(plotRoute[,c("LAT", "LON")]), size = .24, colour = "green")
  }
  else{
    p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data = as.numeric(plotRoute[,c("LAT", "LON")]), size = .24, colour = "red")
  }
}

print(p)


# for (run in 1:rides){
#   temp_ride = data[which(data$Run == run),]
#   dates_ride = unique(temp_ride$ServiceDate)
#   for (k in 1:length(dates_ride)){
#     
#   }
# }