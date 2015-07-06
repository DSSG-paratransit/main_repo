# Modified version of AddLegTimes script that adds a column to a dataframe
# that contains the percent of the total Run time that each lef took.
# Only contains a function -- doesn't actually run it unless you ask


library(dplyr)

# in case the file hasn't already been read
dfr = read.csv("/data/UW_Trip_Data_PassengerC.csv")

# takes a dataframe with ETAs, ServiceDates, and Runs
# returns a dataframe after adding LegTimes and PctTime
getDeadheadPct <- function(dfr) {
  
  # fenceposts
  currentDay = dfr$ServiceDate[1] 
  currentRun = dfr$Run[1]
  ETA = dfr$ETA[1]
  timeTaken = vector(length=nrow(dfr))
  pctTimeTaken = vector(length=nrow(dfr))
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





