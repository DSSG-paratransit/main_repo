#Given some starting and ending points in latitude/longitude, possibly a vector
# of latitude/longitude 
#Get the road distance between two points
library(curl)

dist_matrix_url <- function(lats, lons){
  #get data matrix from open street road map. lons and lats are each 2x1 vectors.
  url = "http://router.project-osrm.org/viaroute?"
  url = paste(url, "loc=", paste(lats[1], lons[1], sep = ","), "&loc=", paste(lats[2], lons[2], sep = ","), sep = "")
  url <- paste(url, "&instructions=false", sep="")
}



