
library(openxlsx)
library(dplyr)
library(timeDate)
library(RJSONIO)
options(digits = 8)

#Get data from the 18 month dataset with headers
fullData <- read.csv("~/UW_Trip_Data_QC4Month.csv")

#This is unncessarry if data is clean
FD_56 = fullData[which(fullData$ProviderId==5 | fullData$ProviderId==6),] #take out 12s
FD_56$Run <-as.character(FD_56$Run) #b/c runs have alpha chars
FD_56 <- FD_56[which(!is.na(FD_56$Run)),] #must have run number
FD_56$ServiceDate <- as.timeDate(as.character(FD_56$ServiceDate)) #make date readable


#Get smaller data to test on, just change FD_56 to SD_56 after next line 
SD_56 <- FD_56[1:23,]

#creates array of all the different runs
rides = unique(FD_56$Run)
#Keeps place in dataframe for updating
place=0
FD_56$legTime <- rep(0, dim(FD_56)[1])
for (ride in rides){ #goes through all the routes
  temp_ride = FD_56[which(FD_56$Run == ride),]
  temp_ride_days = unique(temp_ride$ServiceDate)
  #iterate over one route, different days
  for(k in 1:length(temp_ride_days)){ 
    
      #specifies this_ride as run number from only this day
      this_ride = temp_ride[which(temp_ride$ServiceDate==temp_ride_days[k]),] 
      for (i in 1:length(this_ride)){
        #Finds the legTime based on the next ETA-current ETA for legs in this ride
        FD_56$legTime[place+i]<- this_ride$ETA[i+1]-this_ride$ETA[i]
      }
      
      place=place+length(this_ride)
      
    }
}