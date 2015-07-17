#### This script uses RCurl and RJSONIO to download data from Google's API:
#### Latitude, longitude, location type (see explanation at the end), formatted address
#### Notice ther is a limit of 2,500 calls per day

library(RCurl)
library(RJSONIO)
library(plyr)

url <- function(lat, lon, return.call = "json") {
  root <- "https://maps.googleapis.com/maps/api/distancematrix/"
  n = nrow(lat)
  origins = paste(lat[1],lon[1], sep = ",")
  dests = paste(lat[2], lon[2], sep = ",")
  key = "AIzaSyAIGBjTozWEfIvalGkg7XDWkRvRf97_JFE"
  u <- paste(root, return.call, "?origins=", origins, "&destinations=", dests,"&key=", key, sep = "")
  return(URLencode(u))
}

distanceMatrix <- function(lat, lon,verbose=FALSE) {
  if(verbose) cat(address,"\n")
  u <- url(lat, lon)
  doc <- getURL(u)
  x <- fromJSON(doc,simplify = FALSE)
  if(x$status=="OK") {
    dur <- x$rows[[1]]$elements[[1]]$duration$value
    dist <- x$rows[[1]]$elements[[1]]$distance$value
    return(c(dur, dist))
  } else {
    stop("ERROR: Google Distance Matrix API did not return data.")
  }
}
