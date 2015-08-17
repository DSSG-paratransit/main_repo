library(httr)
library(plyr)
library(timeDate)
library(lattice)
library(ggplot2)
library(ggmap)
library(caret)
library(MASS)

osrm <- function(loc1, loc2){
  'args:
  loc1, loc2: each are 2-tuples of LAT and LON, i.e. c(lat1, lon1), c(lat2, lon2)
  '
  total_times <- numeric(0)
  osrm_url = 'http://router.project-osrm.org/viaroute?'
  lat1 = loc1[1]; lon1 = loc1[2]
  lat2 = loc2[1]; lon2 = loc2[2]
  
  route_url = paste(osrm_url,"loc=",lat1,",", lon1,"&loc=", lat2, ",", lon2, "&instructions=false", sep = "")
  
  json = content(GET(route_url))
  
  time <- json$route_summary$total_time
  dist <- json$route_summary$total_distance
  
  return(list('time' = time, 'dist' = dist))
}

setwd('/home/dssg2015')
data<-read.csv("4moCDT_Part1.csv")

cost_per_sec = 0.805/60
data<-data[which(data$SchedStatus == 1 | NA),]
#data<-data[1:60,]

ride_days = unique(data$ServiceDate)
#Creates array of all the different client IDs
clients = unique(data$ClientID)
#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
costDF <- data.frame(1:11)
costDF <- t(costDF)
colnames(costDF) <- c("ClientCost", "ClientID", "Run", "ServiceDate", 
                      "AvgPass", "LatStart","LonStart", "LatEnd", "LonEnd", 
                      "ClientDist", "ClientTime"
)
costDF<-costDF[-1,]

write.table(costDF, file = "Cost1_Part1.csv", col.names = T, sep = ",", row.names = F)

#clientCost <- numeric((length(clients)))
for(k in 1:length(ride_days)){
  today = data[which(data$ServiceDate==ride_days[k]),]
  today_rides <- unique(today$Run)
  for(kk in 1:length(today_rides)){
    #this_ride occuring on today
    this_ride <- today[which(today$Run == today_rides[kk]),]
    #clients on this_ride
    clients <- na.omit(unique(this_ride$ClientID))
    for (j in 1:length(clients)){
      #instances is one client's routing information
      instances <- which(this_ride$ClientID==clients[j]) #gives rows of today that have clientID == currentClient
      #print(length(instances))
      #analyze only on-boarding (not dropoff)
      #if client has even number of events, and not zero events in the run
      if((length(instances) %% 2 == 0) & (length(instances) !=0)){
        for(jj in 1:(length(instances)/2)){
          PersonOnBus <- this_ride[(instances[(jj*2)-1]:instances[(jj*2)]),]
          onLoc<-c(PersonOnBus[1,17,],PersonOnBus[1,16,])
          offLoc<-c(PersonOnBus[nrow(PersonOnBus),17,],PersonOnBus[nrow(PersonOnBus),16,])
          osrm_out<-osrm(onLoc,offLoc)
          PersonOnBus$PassDist<-osrm_out$dist
          PersonOnBus$PassTime<-osrm_out$time
          rideCost = 0
          avgPass = 0
          for (jjj in 1:(nrow(PersonOnBus)-1)){
            #change leg times var
            rideCost = rideCost + 
              (PersonOnBus$PassTime[jjj]/PersonOnBus$TotalPass[jjj])*(cost_per_sec)
            avgPass = avgPass + PersonOnBus$TotalPass[jjj]
          }
          
          #PersonOnBus$RideCost<-rideCost
          newrow = data.frame(rideCost, clients[j], this_ride$Run[1],
                              as.character(this_ride$ServiceDate[1]),
                              avgPass,
                              PersonOnBus$LAT[(jj*2)-1], PersonOnBus$LON[(jj*2)-1],  
                              PersonOnBus$LAT[(jj*2)], PersonOnBus$LON[(jj*2)],
                              PersonOnBus$PassDist[1], PersonOnBus$PassTime[1]
          )
          #Put all the information from this run on this day for this client in the data frame
          write.table(newrow, file = "Cost1_Part1.csv",
                      col.names = F, append = T, sep = ",", row.names = F)
        }
      }
    }
  }
  print(paste(k/length(ride_days)*100, "% complete", sep =""))
  print(sprintf("day %d of %d unique days", k, length(ride_days)))
  
}

###########
# Open the cost analysis file and analyze CPB info. Be sure to reformat Cost_analysis.csv prior to loading (issue with row indices column)
cost_data <- read.csv("Cost1_Part1.csv", header = T)
cost_data$ServiceDate<-sub('0015',"2015",cost_data$ServiceDate)
cost_data$ServiceDate <- as.Date(as.character(cost_data$ServiceDate))
cost_data <- cost_data[which(cost_data$ClientCost != Inf & !is.na(cost_data$ClientCost)),]
CPB_sub <- cost_data$ClientCost
hist(CPB_sub, breaks = seq(0, 500, 5), xlab = "Costs per boarding ($)", main = "CPB Distribution",
     xaxt = 'n', col = "cyan", ylab = "Number of boardings")
abline(v = quantile(CPB_sub, 0.9), col = "red")
axis(1, at = seq(0,500, 50))
uglyrides <- cost_data[which(CPB_sub>quantile(CPB_sub,0.9)),]
normalrides <- cost_data[which(CPB_sub<=quantile(CPB_sub,0.9)),]
