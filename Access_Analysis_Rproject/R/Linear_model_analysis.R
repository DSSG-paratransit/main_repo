### Make linear regression, regressors vs. total route run time ####
# library(timeDate)

####################################################################################################
############################### Model Building #####################################################
####################################################################################################
meta_data <- read.csv("./data/ride_meta_data.txt", sep = ",")

data <- read.csv("./data/UW_Trip_Data_QC.csv.csv")

# Make matrix of binary contrasts. Every column represents a city, 0 or 1 
# indicates whether a route on a certain day hits a city.
cities <- unique(as.character(data$City))
cities <- cities[cities!=""]
city_mat <- matrix(0, nrow = nrow(meta_data), ncol = length(cities))
data$ServiceDate <- as.timeDate(as.character(data$ServiceDate))
data$Run <- as.character(data$Run)
dates <- unique(data$ServiceDate)
runs <- unique(data$Run)
ctr <- 1
for(ii in 1:length(runs)){
  temp <- data[which(data$Run == runs[ii]),]
  temp_days <- unique(temp$ServiceDate)
  for (kk in 1:length(temp_days)){
    this_run <- temp[which(temp$ServiceDate==temp_days[kk]),]
    visited = unique(this_run$City[this_run$City != ""])
    city_mat[ctr,match(visited, cities)] <- 1
    ctr <- ctr +1
  }
}

city_df <- as.data.frame(city_mat)
colnames(city_df) <- cities

# Total run time is a function of maximum clients serviced, average dwell time, 
# and cities hit.
mod1 <- lm(formula = meta_data$elapsed_time ~ meta_data$max_num_pass + meta_data$avg_dwell_time + city_mat)
sumry <- summary(mod1)
print(sumry)


hist(meta_data$elapsed_time - mod1$fitted.values)
  