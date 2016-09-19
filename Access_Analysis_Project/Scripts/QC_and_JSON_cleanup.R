library(timeDate)
options(digits = 8)

# OVERVIEW:
# (1) Clean up data by removing runs that have zero-ed out lat/lon data,
# have lat/lon data outside of perimeter of WA state, don't finish running
# or simply don't leave the garage
# (2) Further clean data by fixing city names
# (3) Further clean data by removing runs that take longer than 24hrs (there are ~10 of these)
# then make and save a file full of meta data about the runs, for use with regression later on.

# CAVEATS: (1) make sure your data files are in the correct WD: ./data/files. 
# (2) there will be 2 files created, make sure you don't upload to Github.

################### Initial cleaning step: remove obviously bad rides ############################
#delete pre-existing .csv data file
files <- list.files("./data/")
if("UW_Trip_Data_QC.csv" %in% files){file.remove("./data/UW_Trip_Data_QC.csv")}
if (!("AD" %in% ls())){AD = read.csv("./data/UW_Trip_Data.csv")}

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

#Counting number of passengers on bus
passon <- as.character(AD_56$PassOn); passoff <- as.character(AD_56$PassOff)
nOn <- rep(0, length=length(passon)); nOff = nOn
nOn[passon!=""] <- 1; nOff[passoff!=""] <- 1
nOn[AD_56$SchedStatus %in% c(20,21,42)] <- 0
AD_56$nOn <- nOn; AD_56$nOff <- nOff

#Unique dates serviced, unique run numbers
dates = unique(AD_56$ServiceDate)
rides = unique(AD_56$Run)

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
    
    if(this_ride$Activity[1]!=4 | this_ride$Activity[nrow(this_ride)]!=3){
      if(flag != "OK"){
        flag = paste(flag, "ROUTE_FINISH_ERROR", sep = ", ")
      }
      else{
        flag = "ROUTE_FINISH_ERROR"
      }
    }
    
    if(flag == "OK"){
      #Add number of riders
      busCount <- numeric(length = nrow(this_ride))
      for (jj in 1:nrow(this_ride)){
        if (this_ride$Activity[jj]==4){
          busCount[jj] = 0
        }
        else{
          addme = this_ride$nOn[jj]; subme = this_ride$nOff[jj]
          busCount[jj] = busCount[jj-1] + (addme - subme)
        }
      }
      if(ride == rides[1]){
        this_ride$NumPass <- busCount
        write.table(this_ride, file = "./data/UW_Trip_Data_QC.csv", col.names = T, append = T, sep = ",")           
      }
      else{
        this_ride$NumPass <- busCount
        write.table(this_ride, file = "./data/UW_Trip_Data_QC.csv", col.names = F, append = T, sep = ",")
      }
    }
  }
}

############ Second cleaning step: consolidate city names, remove runs in excess of 24hrs ####################
if (!("data" %in% ls())){data <- read.csv("./data/UW_Trip_Data_QC.csv", header = T)}
# headers = c("Rownum", "ServiceDate", "Run", "ProviderId", "EvOrder", 
#             "EvId", "Activity", "ETA", "DwellTime", "StreetNo", "OnStreet", "City",
#             "LON", "LAT", "BookingId", "SchedStatus", "SubtypeAbbr", "FundingsourceId1", "PassOn", "PassOff", "ClientID",
#             "NumOn", "NumOff", "TotalPass")
# colnames(data) <- headers

data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))
data$Run <- as.character(data$Run)
dates <- unique(data$ServiceDate)
runs <- unique(data$Run)

# fix city names. Takes a minute...
data$City <- tolower(as.character(data$City))
for(jj in 1:nrow(data)){
  city_name = data$City[jj]
  if(city_name == "federal waye" | city_name == "federal" | city_name == "fedral way"){
    data$City[jj] <- "federal way"
  }
  if(city_name == "seatle"){ data$City[jj] <- "seattle"}
  if(city_name == "remond"){data$City[jj] <- "redmond"}
  if(city_name == "vashon"){data$City[jj] <- "vashon island"}
  if(city_name == "des monies"){data$City[jj] <- "des moines"}
  if(city_name == "eedmonds"){data$City[jj] <- "edmonds"}
  if(city_name == "lynwood"){data$City[jj] <- "lynnwod"}
  if(city_name == "aubuirn"){data$City[jj] <- "auburn"}
  if(city_name == "bothell-"){data$City[jj] <- "bothell"}
  if(city_name == "kikrland"){data$City[jj] <- "kirkland"}
  if(city_name == "tulwila"){data$City[jj] <- "tukwila"}
  if(city_name == "normandy pk"){data$City[jj] <- "normandy park"}
  if(city_name == "mountlake  terra e"){data$City[jj] <- "mountlake terrace"}
  if(city_name == "burien wa"){data$City[jj] <- "burien"}
  if(city_name == "sea tac"){data$City[jj] <- "seatac"} 
}

#overwrite previously QC'ed data for better quality one.
write.csv(data, file="./data/UW_Trip_Data_QC.csv")

######################## Third step: get ride meta data ##############################
## Get meta_data about each ride. Use for regression later.
## saveme table has runID, date, total elapsed time, maximum number of passengers serviced,
## and average dwell time.
saveme <- matrix(0, nrow = length(dates)*length(runs), ncol = 5)
saveme <- as.data.frame(saveme)
colnames(saveme) <- c("run", "date", "elapsed_time", "max_num_pass", "avg_dwell_time")
ctr = 1
for(ii in 1:length(runs)){
  temp <- data[which(data$Run == runs[ii]),]
  temp_days <- unique(temp$ServiceDate)
  for (kk in 1:length(temp_days)){
    this_run <- temp[which(temp$ServiceDate==temp_days[kk]),]
    this_run <- this_run[-which(this_run$Activity !=3), ]
    elapsed <- this_run$ETA[nrow(this_run)] - this_run$ETA[1]
    max_pass <- max(this_run$TotalPass)
    avg_dwell <- mean(this_run$DwellTime)
    saveme[ctr,] <- c(runs[ii], as.character(temp_days[kk]), elapsed, max_pass, avg_dwell)
  }
}

saveme <- saveme[which(saveme$elapsed_time < 86400),]

#Save file. Don't post on Github!!!!
write.table(x = saveme, file = "./data/ride_meta_data.txt", sep = ",")





