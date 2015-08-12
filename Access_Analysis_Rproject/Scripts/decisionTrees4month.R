##### Attempt to make decision trees for the 4-month ugly-ride data (QC4mo_and_cost)
library(lubridate)
options(digits = 9)
setwd('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/Scripts/')
source('osrm_function.R')

##################### Get data of interest for classifying ugly runs ######################

#load data. Make ServiceDate column Date type, correct the years, get just pickups and dropoffs.
colclasses = c("Date", "character", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "character", "character","numeric", "numeric", "numeric", "numeric", "factor", "numeric", "character", "character", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric")
if (!('fourMo' %in% ls())){
  fourMo <- read.table('../data/QC4mo_and_cost.csv', sep = ',', header = T, stringsAsFactors = F, colClasses = colclasses)}
dataOnOff <- fourMo[which(fourMo$Activity == 1 | fourMo$Activity == 0),]
dataOnOff$ServiceDate <- as.Date(as.character(dataOnOff$ServiceDate))
year(dataOnOff$ServiceDate) <- year(dataOnOff$ServiceDate)+2000
dataOnOff$BookingId <- dataOnOff$BookingId

#if city is missing, get rid of it. If person is no-show, get rid of row. Also reindex dataOnOff.
dataOnOff <- dataOnOff[which(dataOnOff$City != ""),]
dataOnOff <- dataOnOff[which(dataOnOff$SchedStatus != 20),]
rownames(dataOnOff) <- 1:nrow(dataOnOff)

#add OffCity column to data:
OnCity <- vector(mode = 'character', length = nrow(dataOnOff))
OffCity <- vector(mode = 'character', length = nrow(dataOnOff))
OnLat <- vector(mode = 'numeric', length = nrow(dataOnOff))
OnLon <- OnLat; OffLat <- OnLat; OffLon <- OnLat
TimeOfDay <- OnLat
Wday <- OnLat #0 for DayOfWeek implies weekend, 1 means weekday
TimeOnBus <- OnLat

#Each BookingId already has an 'OnCity', so give each BookingId an "OffCity" city.
NArows <- numeric(0); NActr <- 1
for (i in 1:50000){ #0 is on, 1 is off.
  if (dataOnOff$Activity[i] == 0){
    current_row = dataOnOff[i,]
    thisId <- current_row$BookingId
    OnCity[i] <- current_row$City
    TimeOfDay[i] <- current_row$ETA
    dwk <- wday(current_row$ServiceDate)
    if (dwk == 7 | dwk == 1){
      Wday[i] <- 0
    }
    else{
      Wday[i] <- 1
    }
    search_data <- dataOnOff[(i+1):(i+40),]
    match_ind = which(search_data$BookingId == thisId)
    if (length(match_ind) ==1){
      OffCity[i] <- search_data$City[match_ind]
      OffLat[i] <- search_data$LAT[match_ind]
      OffLon[i] <- search_data$LON[match_ind]
      TimeOnBus[i] <- search_data$ETA[match_ind] - current_row$ETA
    }
    else if (length(match_ind)!=1){
      NArows[NActr] <- i
      NActr <- NActr+1
    }
  }
}

dataOnOff$OnCity <- OnCity; dataOnOff$OffCity <- OffCity
dataOnOff$OffLat <- OffLat
dataOnOff$OffLon <- OffLon
dataOnOff$TimeOfDay <- TimeOfDay
dataOnOff$TimeOnBus <- TimeOnBus
dataOnOff$Wday <- Wday

dataOnOff <- dataOnOff[-NArows,]
dataOnOff <- dataOnOff[which(dataOnOff$Activity == 0),]
cut_ind <- which(dataOnOff$TimeOnBus == 0)[1]
dataOnOff <- dataOnOff[1:(cut_ind-1),]


############################ Decision tree analysis ######################
library(rpart)

#organize tree data, scale the TimeOnBus variable, make cities categorical vars
treeData <- dataOnOff[,c("ClientCost", "Ugly", "OnCity", "OffCity","TimeOfDay", "Wday", "Ugly")]
treeData$ClientCost <- scale(treeData$ClientCost)
treeData$TimeOfDay <- treeData$TimeOfDay-min(treeData$TimeOfDay)
treeData$OnCity <- as.factor(treeData$OnCity)
treeData$OffCity <- as.factor(treeData$OffCity)
treeData <- treeData[!is.na(treeData$Ugly),]

# grow tree 
fit <- rpart(Ugly ~ OnCity + OffCity + TimeOfDay+ Wday,
             method="class", data = treeData)

print(fit$cptable[,'rel error'])
#No results!!! BOOOOOOOOOOO

pfit<- prune(fit, cp=   fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])

plot(pfit, uniform=TRUE, 
     main="Pruned Classification Tree for Ugly Rides")
text(pfit, use.n=TRUE, all=TRUE, cex=.8)

