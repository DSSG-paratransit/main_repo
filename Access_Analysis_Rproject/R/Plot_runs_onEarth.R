library(ggmap)
library(timeDate)
cols = c("ServiceDate", "Run", "ProviderId", "EvOrder", "EvId", "Activity", "ETA", "DwellTime",
             "StreetNo", "OnStreet", "City", "LON", "LAT", "BookingId", "SchedStatus",
             "SubtypeAbbr", "FundingSourceId1", "PassOn", "PassOff", "ClientId")
data <- read.csv("UW_Trip_Data_QC.csv", nrows = 100000)
colnames(data) <- cols
colnames(data)<- c("row.number", cols)
data$Run <- as.character(data$Run)
data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))

dates = unique(data$ServiceDate)
my_date = sample(dates, 1)
temp_date_data <- data[which(data$ServiceDate==my_date),]
runs = unique(temp_date_data$Run)
my_run = sample(runs,1)
temp = temp_date_data[which(temp_date_data$Run == my_run),]

lons = temp$LON
lats = temp$LAT
if (length(lons)>20){
  zm = 11
} else {
  zm = 10
}

center_King_Co = c(mean(lons), mean(lats))
map <- get_googlemap(center = center_King_Co, zoom = 10, maptype = "roadmap")

p <- ggmap(map)+
geom_point(aes(x = lons, y = lats), data = temp, size = sqrt(2), colour = "black")+
geom_segment(aes(x = lons[1], y = lats[1], xend = lons[2], yend = lats[2]), data = temp, size = .24, colour = "red")
for (j in 2:(length(lons)-1)){
  print(j)
  if (j != length(lons)-1){
    p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data=temp, size = .24, colour = "green")
  }
  else{
    p <- p + geom_segment(x = lons[j], y = lats[j], xend = lons[j+1], yend = lats[j+1],data = temp, size = .24, colour = "red")
  }
}

p
