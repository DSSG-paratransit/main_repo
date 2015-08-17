library(httr)
library(plyr)
library(timeDate)
library(MASS)
options(digits=9)

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

data <- read.csv('UW_Trip_Data_4mo_CDT.csv')
cost_per_sec = 0.805/60
data<-data[which(data$SchedStatus == 1),]
data$ServiceDate <- as.character(data$ServiceDate)
data$Run <- as.character(data$Run)
data$City <- as.character(data$City)

ride_days = unique(data$ServiceDate)
#Creates array of all the different client IDs
bookingids = unique(data$ClientID)
#Set up dataframe that I'll use
#I'll need clientCost, clientID, Run, ServiceDate, LatStart, LonStart, LatEnd, LonEnd
costDF <- data.frame(1:8)
costDF <- t(costDF)
colnames(costDF) <- c("ClientCost", "ClientID", "Run", "ServiceDate", 
                      "osrm_ClientDist", "osrm_ClientTime", 'OnCity', 'OffCity'
)
costDF<-costDF[-1,]

write.table(costDF, file = "CPBAnalysis.csv", col.names = T, sep = ",", row.names = F)

for(k in 1:length(ride_days)){
  today = data[which(data$ServiceDate==ride_days[k]),]
  today_rides <- unique(today$Run)
  for(kk in 1:length(today_rides)){
    #this_ride occuring on today
    this_ride <- today[which(today$Run == today_rides[kk]),]
    #clients on this_ride
    bookingids <- unique(this_ride$BookingId) #none of the bookingIDs are NA.
    for (j in 1:length(bookingids)){
      #instances is one client's routing information
      instances <- which(this_ride$BookingId==bookingids[j]) #gives rows of today that have clientID == currentClient
      #print(length(instances))
      #analyze only on-boarding (not dropoff)
      #if client has even number of events, and not zero events in the run
      if((length(instances) %% 2 == 0) & (length(instances) !=0)){
        for(jj in 1:(length(instances)/2)){
          PassDist = numeric(0)
          PersonOnBus <- this_ride[(instances[(jj*2)-1]:instances[(jj*2)]),]
          Time_Vec <- diff(PersonOnBus$ETA) #amount of time between two nodes
          onLoc<-c(PersonOnBus[1,'LAT'],PersonOnBus[1,'LON'])
          offLoc<-c(PersonOnBus[nrow(PersonOnBus),'LAT'],PersonOnBus[nrow(PersonOnBus),'LON'])
          osrm_out<-osrm(onLoc,offLoc)
          osrmDist<-osrm_out$dist
          osrmTime<-osrm_out$time
          OnCity <- PersonOnBus$City[1]
          OffCity <- PersonOnBus$City[nrow(PersonOnBus)]
          rideCost = 0
          for (jjj in 1:(nrow(PersonOnBus)-1)){
            #change leg times var
            rideCost = rideCost + 
              (Time_Vec[jjj]/PersonOnBus$TotalPass[jjj])*(cost_per_sec)
          }
          
          #PersonOnBus$RideCost<-rideCost
          newrow = data.frame(c(rideCost, bookingids[j], this_ride$Run[1],
                                as.character(this_ride$ServiceDate[1]),
                                osrmDist, osrmTime, OnCity, OffCity)
          )
          #Put all the information from this run on this day for this client in the data frame
          write.table(t(newrow), file = "CPBAnalysis.csv",
                      col.names = F, append = T, sep = ",", row.names = F)
        }
      }
    }
  }
  print(paste(k/length(ride_days)*100, "% complete", sep =""))
  print(sprintf("day %d of %d unique days", k, length(ride_days)))
}


