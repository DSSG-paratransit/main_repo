# strip the dummy coefficients for each city from the model
# replace insignificant coefficients with NA
city_coefs <- {}
for (i in seq(3:51)){
  city_coefs[i]<-mod1$coefficients[i]
  if (summary(mod1)$coefficients[,4][i]>.05)
    city_coefs[i]<-NA 
}

# rank city coefficients from highest to lowest
city_rank<-order(city_coefs, decreasing=FALSE)
names(city_rank)<-cities
# show high/low cost cities
# high cost
high_cost<-which(city_rank<10)
high_cost_cities<-names(city_rank)[city_rank<10]

for (i in high_cost_cities){
  print(mean(meta_data$avg_dwell_time))
}


# low cost
low_cost<-which(city_rank>40)
low_cost_cities<-names(city_rank)[city_rank>40]

# subset the columns by city row (high/low)
# extract the low city columns of matrix
# if the rowsum for a run is 1 add to mean calculation for high/low dwell time
# for each run #, find what cities where passed through
for (low_cost_cities)
  summary(meta_data$avg_dwell_time)

if (cities=="kent")
  summary(meta_data$avg_dwell_time)
