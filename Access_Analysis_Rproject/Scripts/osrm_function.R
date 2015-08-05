library(httr)

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