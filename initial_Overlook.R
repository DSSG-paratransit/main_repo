library(openxlsx)
library(dplyr)
library(timeDate)
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
# AD_56 has no missing route ID's, only has Access bus driver provider info,
# and starts with a route that is just leaving a garage.

#Check to see if 3's are followed by 4's and to see if 4's are preceded by 3's
for (i in 2:(nrow(AD_56)-1)){
  if ((AD_56$Activity[i] == 3) && (AD_56$Activity[i+1] != 4)){
    sprintf("Error: Activity in row %s is 3 and following row is not 4\n", i)}
  if ((AD_56$Activity[i] == 4) && (AD_56$Activity[i-1] != 3)){
    sprintf("Error: Activity in row %s is 4 and preceding row is not 3\n", i)}
}

#Check to see if any LAT/LON data missing:
if(any(is.na(AD_56$LON))){
  print("No Longitude data missing.\n")
}
if(any(is.na(AD_56$LAT))){
  print("No Latitude data missing.\n")
}


#Check to see if any routes run more than once in a day. This is not the case.
dates = unique(AD_56$ServiceDate)
for (day in dates){
  temp_day = AD_56[which(AD_56$ServiceDate == day),]
  dayrides = unique(temp_day$Run)
  for(ride in dayrides){
    temp_ride = temp_day[which(temp_day$Run==ride),]
    rs = as.numeric(rownames(temp_ride))
    start_ride_row =rs[1]; num_straight_stops = length(rs)-1
    if((start_ride_row+num_straight_stops) != rs[length(rs)]){
      sprintf("WARNING: Ride %s ran more than once on day %s", ride, day)
    }
  } 
}





