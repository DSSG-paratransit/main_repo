library(openxlsx)
library(dplyr)
library(timeDate)
library(RJSONIO)
options(digits = 8)

#delete pre-existing .csv data file
files <- list.files()
if("UW_Trip_Data_QC.csv" %in% files){file.remove("UW_Trip_Data_QC.csv")}
if (!("AD" %in% ls())){AD = read.csv("UW_Trip_Data.csv")}

AD_56 = AD[which(AD$ProviderId==5 | AD$ProviderId==6),]
AD_56$Run <-as.character(AD_56$Run)
AD_56 <- AD_56[which(!is.na(AD_56$Run)),]
AD_56$ServiceDate <- as.timeDate(as.character(AD_56$ServiceDate))

ctr = 1; activ = AD_56$Activity[ctr]
while(activ != 4){
  ctr = ctr+1
  activ = AD_56$Activity[ctr]
}
AD_56 = AD_56[-(1:(ctr-1)),]

#Compute ECDF of distance per leg
dates = unique(AD_56$ServiceDate)
rides = unique(AD_56$Run)
ETA_hist_vec = numeric(1)
Dists_hist_vec = ETA_hist_vec

#Haversine formula: "As the crow flies" distance
deg2rad <- function(deg){return(deg*pi/180)}
gcd.hf <- function(lat, lon){
  long1 <- deg2rad(lon[1]); long2 <- deg2rad(lon[2])
  lat1 <- deg2rad(lat[1]); lat2 <- deg2rad(lat[2])
  R <- 6371 # Earth mean radius [km]
  delta.long <- (long2 - long1)
  delta.lat <- (lat2 - lat1)
  a <- sin(delta.lat/2)^2 + cos(lat1) * cos(lat2) * sin(delta.long/2)^2
  c <- 2 * asin(min(1,sqrt(a)))
  d = R * c
  return(d) # Distance in km
}

#Coordinate boundaries of King County, WA:
upper_right <- c(49.020430, -116.998768)
lower_left <- c(45.606961, -124.974842)
minlat = lower_left[1]; maxlat = upper_right[1]
minlon = lower_left[2]; maxlon = upper_right[2]

#Flag routes accordingly
for (ride in rides){ #iterate over every instance of a route
  temp_ride = AD_56[which(AD_56$Run == ride),]
  temp_ride_days = unique(temp_ride$ServiceDate)
  for(k in 1:length(temp_ride_days)){ #iterate over one route, different days
    flag = "OK"
    this_ride = temp_ride[which(temp_ride$ServiceDate==temp_ride_days[k]),]
    lat_coords = this_ride$LAT; lon_coords = this_ride$LON
    if(any(lat_coords<minlat) | any(lat_coords>maxlat) | any(lon_coords<minlon) | any(lon_coords>maxlon)){
      flag = "BAD_COORDS"
    }
    for(kk in 1:nrow(this_ride)){
      if((!is.na(this_ride$BookingId[kk])) & (is.na(this_ride$ClientId[kk]))){
        if(flag != "OK"){
          flag = paste(flag, "MISSING_CLIENTID", sep = ", ")
        }
        else{
          flag = "MISSING_CLIENTID"
        }
      }
    }
    if(all(this_ride$LON==this_ride$LON[1])){
      flag = "NO_MOVEMENT"
    }
    
    Durs = numeric(nrow(this_ride)-1)
    Dists = numeric(nrow(this_ride)-1)
    for (leg in 2:nrow(this_ride)){
      lat = c(this_ride$LAT[leg-1], this_ride$LAT[leg]); lon = c(this_ride$LON[leg-1], this_ride$LON[leg])
      Durs[leg-1] = this_ride$ETA[leg]-this_ride$ETA[leg-1]
      Dists[leg-1] = gcd.hf(lat, lon)
    }
    
    if(this_ride$Activity[1]!=4 | this_ride$Activity[nrow(this_ride)]!=3){
      if(flag != "OK"){
        flag = paste(flag, "ROUTE_FINISH_ERROR", sep = ", ")
      }
      else{
        flag = "ROUTE_FINISH_ERROR"
      }
    }
    
    if(flag == "OK"){
      ETA_hist_vec <- c(ETA_hist_vec, Durs)
      Dists_hist_vec <- c(Dists_hist_vec, Dists)
      write.table(this_ride, file = "UW_Trip_Data_QC.csv", col.names = F, append = T, sep = ",")
    }
    
#     LATs = this_ride$LAT; LONs = this_ride$LON
#     SCHEDs = this_ride$SchedStatus
#     CLIENTIDs = this_ride$ClientId
#     ride_list = list(ROUTE = ride, DATE = as.character(temp_ride_days[k]), FLAG = flag, DURATIONS = Durs, EUCLID_DISTS = Dists,
#                      LAT = LATs, LON = LONs, SCHED_STAT = SCHEDs, CLIENTID = CLIENTIDs, PASSON = as.character(this_ride$PassOn),
#                      PASSOFF = as.character(this_ride$PassOff), ETA = this_ride$ETA, ACTIVITY = this_ride$Activity)
#     write(toJSON(ride_list), "UW_Trip_QC.json", append = T)
  }
}

# #Plot ATCF distances/time of legs
# plot(log(ETA_hist_vec), Dists_hist_vec,
#     xlab = "Time", ylab = "Euclidean Distance", main= "Time vs. Distance Scatterplot",
#     pch = 21, bg = "red")
# 
# #Note outliers: time splits range from 0 to 304201. 99.5% quantile is 7824.4 seconds.
# plot(ecdf(ETA_hist_vec[which(ETA_hist_vec < quantile(ETA_hist_vec, .999))]/60),
#      xlab = "Minutes", ylab = "ECDF of Stop Splits", main = "ECDF of Travel Times between Stops")






