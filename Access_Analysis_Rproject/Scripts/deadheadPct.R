# Modified version of AddLegTimes script that adds a column to a dataframe
# that contains the percent of the total Run time that each leg took.
# Only contains functions -- doesn't actually run them unless you ask

#DOES NOT ALWAYS WORK CORRECTLY
#we're still unsure why the percentages aren't always correct


library(dplyr)

# in case the file hasn't already been read
#dfr = read.csv("data/UW_Trip_Data_PassengerC.csv")


# takes a dataframe with ETAs, ServiceDates, and Runs
# returns a dataframe after adding LegTimes and PctTime
getDeadheadPct <- function(dfr) {
  
  # fenceposts
  currentDay = dfr$ServiceDate[1] 
  currentRun = dfr$Run[1]
  ETA = dfr$ETA[1]
  timeTaken = vector(length=nrow(dfr))
  pctTimeTaken = vector(length=nrow(dfr))
  totalPCT = vector(length=nrow(dfr))
  totalRouteTime = 0 #time that the current route has taken
  baseRow = 1 #the row number in which the current run left base
  
  for(i in 1:nrow(dfr)) {
    leftAt = ETA
    ETA = dfr$ETA[i]
    previousDay = currentDay
    previousRun = currentRun
    currentDay = dfr$ServiceDate[i]
    currentRun = dfr$Run[i]
    
    # if row is when bus leaves base the 'previous' segment took 0s
    # calculates the pct time taken, adds to vector 
    if (previousDay != currentDay) {
      pctTimeTaken[baseRow:(i-1)] = timeTaken[baseRow:(i-1)]/totalRouteTime
      totalRouteTime = 0
      time = 0
    } else if (previousRun != currentRun) {
      pctTimeTaken[baseRow:(i-1)] = timeTaken[baseRow:(i-1)]/totalRouteTime
      totalRouteTime = 0
      time = 0
    } else if (i==nrow(dfr)) { #for case where it is the last run in the dataset 
      pctTimeTaken[baseRow:(i-1)] = timeTaken[baseRow:(i-1)]/totalRouteTime
      totalRouteTime = 0
      time = 0
    } else {
      time = ETA - leftAt 
    }
    timeTaken[i] = time
    totalRouteTime = totalRouteTime + time
  }
  
  # adds new vector to dataframe and returns
  dfr$PctTime <- pctTimeTaken
  dfr$LegTime <- timeTaken
  return(dfr)
}

#dfr <- getDeadheadPct(dfr)

#Used with the deadheadPct script to keep track of the total
# percent of the time that has been accounted for 
# Only works when the dataframe already has the PctTime column
# This was originally created because deadheadPCt was not working
# correctly, and it was used to try to figure out when/why it was breaking


getTotalPCT <- function(dfr) {
  totalPCT = vector(length=nrow(dfr))
  totalPCT[1]=0
  currentRun = dfr$Run[1]
  for (i in 2:nrow(dfr)){
    previousRun = currentRun
    currentRun = dfr$Run[i]
    if (previousRun != currentRun) {
      totalPCT[i]=0
    } else {
      totalPCT[i]=dfr$PctTime[i]+totalPCT[i-1]
    }
    
  }
  dfr$totalPCT <- totalPCT
  return(dfr)
}



######################Emily's random notes when trying to get it to work

#Percents still don't work correctly all the time, don't always add up to 100%

#16682
#run 8708 adds to .65 total percent--that's good....

#dfrShort <- rohansData[1:855, ] 
#dfrShort <- getDeadheadPct(dfrShort)
#dfrShort <- getTotalPCT(dfrShort)


#dfr1 <- rohansData
#dfr1 <- getDeadheadPct(dfr1)
#dfr1 <- getTotalPCT(dfr1)

#dfr8708 <- rohansData[which(rohansData$Run == 9701),]
#dfr8708 <- getDeadheadPct(dfr8708)
#dfr8708 <- getTotalPCT(dfr8708)



