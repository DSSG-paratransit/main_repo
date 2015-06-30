dataFrame = read.csv("data/UW_Trip_Data_QC.csv")

passengerCount = 0
passengerCounts = vector(length=nrow(dataFrame))
currentDay = dataFrame$ServiceDate[1]
currentRun = dataFrame$Run[1]

for(i in 1:nrow(dataFrame)) {
  previousDay = currentDay
  previousRun = currentRun
  currentDay = dataFrame$ServiceDate[i]
  currentRun = dataFrame$Run[i]
  
  if(previousRun != currentRun) {
    passengerCount = 0
  }
  
  if(previousDay != currentDay) {
    passengerCount = 0
  }
  
  if(grepl("CLI1", dataFrame$PassOn[i])) {
    passengerCount = passengerCount + 1
  }
  
  if(grepl("CLI1", dataFrame$PassOff[i])) {
    passengerCount = passengerCount - 1
  }
  
  print(i)
  print(passengerCount)
  passengerCounts[i] = passengerCount
}

dataFrame$PassengersOnBoard = passengerCounts

write.csv(dataFrame, 'data/UW_Trip_Data_PassengerC.csv')

