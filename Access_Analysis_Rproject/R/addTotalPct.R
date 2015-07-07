#Used with the deadheadPct script to keep track of the total
# percent of the trime that has been accounted for 
# Only works when the dataframe already has the PctTime column

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
