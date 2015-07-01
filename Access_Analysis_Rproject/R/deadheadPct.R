library(dplyr)

df = read.csv("data/UW_Trip_Data_PassengerC.csv")

getDeadheadPct <- function(dfr) {
  currentDay = dfr$ServiceDate[1]
  currentRun = dfr$Run[1]
  ETA = dfr$ETA[1]
  timeTaken = vector(length=nrow(dfr))
  
  for(i in 1:nrow(dfr)) {
    leftAt = ETA
    ETA = dfr$ETA[i]
    previousDay = currentDay
    previousRun = currentRun
    currentDay = dfr$ServiceDate[i]
    currentRun = dfr$ServiceRun[i]
    if (previousDay != currentDay) {
      time = 0
    } else if (previousRun != currentRun) {
      time = 0
    } else {
      time = ETA - leftAt 
    }
    timeTaken[i] = time
  }
  return(timeTaken)
}


oneDay = filter(df, ServiceDate==ServiceDate[1])
oneRun = filter(oneDay, Run==Run[1])




