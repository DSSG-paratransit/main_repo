getLegTimeDist <- function(data) {
  
  # fenceposts
  currentDay = data$ServiceDate[1] 
  currentRun = data$Run[1]
  lat<-data$LAT[1] 
  lon<-data$LON[1]
  loc = c(lat, lon)
  time_vector = vector(length=nrow(data))
  dist_vector = vector(length=nrow(data))
  
  for(i in 1:nrow(data)) {
    previousLoc = loc
    lat<-data$LAT[i] 
    lon<-data$LON[i]
    loc = c(lat, lon)
    previousDay = currentDay
    previousRun = currentRun
    currentDay = data$ServiceDate[i]
    currentRun = data$Run[i]
    
    # hard coding time and distance to 0 if row changes to different day/run
    if (previousDay != currentDay) {
      time = 0
      dist = 0
    } else if (previousRun != currentRun) {
      time = 0
      dist = 0
      
    }  
    
    # calculate distance between previous location and current location with osrm_function.R
    else {
      osrm_output<-osrm(previousLoc, loc)
      time = osrm_output[1] 
      dist = osrm_output[2]
    }
    time_vector[i] = time
    dist_vector[i] = dist
    
  }
  
  # adds distance and time vectors to dataframe and returns
  data$Dist <- dist_vector
  data$Time <- time_vector
  return(data)
}
