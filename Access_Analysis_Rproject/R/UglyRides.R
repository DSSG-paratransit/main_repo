#Ugly rides:
# We need something to look for each clientID,
# for a given day
# find the legs that the client is on the bus, excluding the one where he gets off
# the number of minutes that each leg he was on took/number of clients on the bus
# then add that to a running total for costOfClientID
#


 ride_days = unique(AD_56$ServiceDate)
 clients = unique(ride_days$ClientId)
 for(k in 1:length(ride_days)){ 
    today = AD_56[which(AD_56$ServiceDate==ride_days[k]),]
    AD_56[which(AD_56$ClientId)]
    filter(AD_56, ServiceDay=)

 }
 for(day in ride_days){
   for(client in clients){
      filter(AD_56, ServiceDay=day, ClientId=client )
   }
 }
 filter(AD_56, ServiceDay=)