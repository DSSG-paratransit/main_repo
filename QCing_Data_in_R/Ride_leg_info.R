library(dplyr)
library(timeDate)
source("Google_API_Integration.R")

#Clean up data, get subset for analysis.
AD = read.csv("UW_Trip_Data2SmallChunk_CSV.csv")
AD_56 = AD[which(AD$ProviderId==5 | AD$ProviderId==6),]
AD_56$Run <- as.numeric(as.character(AD_56$Run))
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

for (ride in rides){
  temp_ride = AD_56[which(AD_56$Run == ride),]
  temp_ride_days = unique(temp_ride$ServiceDate)
  for(k in 1:length(temp_ride_days)){
    this_ride = temp_ride[which(temp_ride$ServiceDate==temp_ride_days[k]),]
    Durs = numeric(nrow(this_ride))
    Dists = numeric(nrow(this_ride))
    #Get distance/times of each leg of ride
    for (leg in 2:nrow(this_ride)){
      lat = c(this_ride$LAT[leg-1], this_ride$LAT[leg]); lon = c(this_ride$LON[leg-1], this_ride$LON[leg])
      #dur_dist = distanceMatrix(lat, lon)
      Durs[leg-1] = this_ride$ETA[leg]-this_ride$ETA[leg-1]
      Dists[leg-1] = gcd.hf(lat, lon)
      #Dists[leg-1] = dur_dist[2]
    }
    #ride_list = list(route = ride, date = as.character(day), leg_durations = Durs, leg_distances = Dists)
    #write(toJSON(ride_list), "ride_leg_info.json", append = T)
    ETA_hist_vec = c(ETA_hist_vec, Durs)
    Dists_hist_vec = c(Dists_hist_vec, Dists)
    ride_list = list(route = ride, date = as.character(temp_ride_days[k]), leg_durations = Durs, leg_distances = Dists)
    write(toJSON(ride_list), "ride_leg_info.json", append = T)
  }
}


#Plot ATCF distances/time of legs
rm_me = c(which(is.na(Dists_hist_vec)), which(Dists_hist_vec>100))
Dists_cln <- Dists_hist_vec[-rm_me]; ETA_cln <- ETA_hist_vec[-rm_me]
plot(ETA_cln[which(Dists_cln!=0 & ETA_cln<8000)], Dists_cln[which(Dists_cln != 0 & ETA_cln<8000)],
    xlab = "Time", ylab = "Euclidean Distance", main= "Time vs. Distance Scatterplot",
    pch = 21, bg = "red")
plot(ecdf(ETA_cln[which(Dists_cln!=0 & ETA_cln<8000)]))






