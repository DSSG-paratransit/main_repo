getLegTimeDist <- function(data) {
  
  # fenceposts
  currentDay = data$ServiceDate[1] 
  currentRun = data$Run[1]
  lat<-data$LAT[i] 
  lon<-data$LON[i]
  loc = c(lat, lon)
  time_vector = vector(length=nrow(data))
  dist_vector = vector(length=nrow(data))
  baseRow = 1 #the row number in which the current run left base
  
  for(i in 1:nrow(data)) {
    previousLoc = loc
    lat<-data$LAT[i] 
    lon<-data$LON[i]
    loc = c(lat, lon)
    previousDay = currentDay
    previousRun = currentRun
    currentDay = data$ServiceDate[i]
    currentRun = data$Run[i]
    
    # if row is when bus leaves base the 'previous' segment took 0s
    # calculates the pct time taken, adds to vector 
    if (previousDay != currentDay) {
      time = 0
      dist = 0
    } else if (previousRun != currentRun) {
      time = 0
      dist = 0
      
    }  
    
    else {
      osrm_output<-osrm(previousLoc, loc)
      time = osrm_output[1] 
      dist = osrm_output[2]
    }
    time_vector[i] = time
    dist_vector[i] = dist
    
  }
  
  # adds new vector to dataframe and returns
  data$Dist <- dist_vector
  data$Time <- time_vector
  return(data)
}
