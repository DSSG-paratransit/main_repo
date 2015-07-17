library(openxlsx)
library(dplyr)
library(timeDate)
library(RJSONIO)
options(digits = 8)

# add leg times to any dataframe df
# returns the modified dataframe
legTimes <-function(df) {
  currentDay = df$ServiceDate[1]
  currentRun = df$Run[1]
  ETA = df$ETA[1]
  timeTaken = vector(length=nrow(df))
  for(i in 1:nrow(df)) {
    leftAt = ETA
    ETA = df$ETA[i]
    previousDay = currentDay
    previousRun = currentRun
    currentDay = df$ServiceDate[i]
    currentRun = df$Run[i]
    
    # if row is signals when bus leaves base 
    # the 'previous' segment took 0s
    if (previousDay != currentDay) {
      time = 0
    } else if (previousRun != currentRun) {
      time = 0
    } else {
      time = ETA - leftAt 
    }
    timeTaken[i] = time
  }
  df$LegTime <- timeTaken
  return(df)
}

#Get data from the dataset with headers
fullData <- read.csv("~/UW_Trip_Data_QC4Month.csv")

#This is unncessarry if data is clean
FD_56 = fullData[which(fullData$ProviderId==5 | fullData$ProviderId==6),] #take out 12s
FD_56$Run <-as.character(FD_56$Run) #b/c runs have alpha chars
FD_56 <- FD_56[which(!is.na(FD_56$Run)),] #must have run number
FD_56$ServiceDate <- as.timeDate(as.character(FD_56$ServiceDate)) #make date readable


#Get smaller data to test on, just change FD_56 to SD_56 after next line 
SD_56 <- FD_56[1:23,]

# apply legTime funtion to dataFrame
FD_56 <- legTime(FD_56)
