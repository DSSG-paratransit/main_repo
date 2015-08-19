setwd('/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/Scripts/')
data18 <- read.csv('../data/UW_Trip_Data_FullHeaders.csv')
library(lubridate)

Dates <- as.Date(strptime(data18$ServiceDate, format = "%m/%d/%Y %H:%M:%S"))
data18$ServiceDate <- Dates

alldays <- seq(from = min(Dates), to = max(Dates), by = 1)
schstats <- data18[,c('ServiceDate', 'Activity')]
oos_stor <- numeric(length = length(alldays))
ctr = 1
for (day in alldays){
  today <- schstats[which(schstats$ServiceDate == day),]
  oos_stor[ctr] <- sum(today$Activity == 8)
  ctr = ctr +1
  cat("On date: ",day)
}

dayofweek_vec <- wday(alldays)
output <- cbind(as.character(alldays), oos_store, dayofweek_vec)
output <- as.data.frame(output)
colnames(output) <- c('Date', 'oos_counts', 'dayofweek')
output$oos_counts <- as.numeric(output$oos_counts)
output$dayofweek <- as.numeric(output$dayofweek)
output$dayofweek[output$dayofweek == 1] <- 'Sunday'
output$dayofweek[output$dayofweek == 2] <- 'Monday'
output$dayofweek[output$dayofweek == 3] <- 'Tuesday'
output$dayofweek[output$dayofweek == 4] <- 'Wednesday'
output$dayofweek[output$dayofweek == 5] <- 'Thursday'
output$dayofweek[output$dayofweek == 6] <- 'Friday'
output$dayofweek[output$dayofweek == 7] <- 'Saturday'

write.csv(x = output, file = '../data/code8_counts.csv', row.names = F)

#Anova test and boxplots:
library(ggplot2)
summary(aov(dayofweek ~ oos_counts, data = output))
boxplot(oos_counts ~dayofweek, data = output, xaxt = 'n', ylab = 'Out-of-service events', main = 'Boxplots of out-of-service events by day')
  axis(side = 1, at = c(1:7), labels = c("Sunday", "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday"), las = 2)
ggplot(data = output, aes(x = dayofweek, y= oos_counts))+geom_boxplot(aes(fill = dayofweek)) + xlab("")+ylab("Out-of-service counts")+ggtitle("Out-of-service boxplots by day of week\n18 month data")+theme(legend.position="none")

# paired t.test to see if there's meaningful difference between monday and friday out-of-service codes:
t.test(output$oos_counts[output$dayofweek=='Monday'], output$oos_counts[output$dayofweek=='Friday'][1:73], paired = T)
t.test(output$oos_counts[output$dayofweek=='Monday'], output$oos_counts[output$dayofweek=='Tuesday'][1:73], paired = T)
t.test(output$oos_counts[output$dayofweek=='Monday'], output$oos_counts[output$dayofweek=='Wednesday'][1:73], paired = T)

#not significant, possibly with more data though.


#find stats about number of breakdowns over different days of the week. 1 = Sunday, 7 is Saturday.
output[,'oos_counts']<- as.numeric(output[,'oos_counts'])
dayofweek <- c(1:7)
dow_stor <- matrix(NA, nrow = 7, ncol = 5)
for (d in dayofweek){
  same_dow <- as.numeric(output[which(wday(output[,'Date'])==d),2])
  dow_stor[d, 1] <- d
  dow_stor[d, 2] <- sum(same_dow)
  dow_stor[d, 3] <- mean(same_dow)
  dow_stor[d, 4] <- sd(same_dow)
  dow_stor[d, 5] <- length(same_dow)
}

dow_stor <-as.data.frame(dow_stor)
colnames(dow_stor) <- c("dow", "n_8s", "Mean_OOS", "SD_OOS", "n_obs")
dow_stor$dow <- c("Sunday", "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday")
