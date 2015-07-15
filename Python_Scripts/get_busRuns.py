def get_busRuns.py(data, Run, resched_init_time):
	''' take pd.DataFrame from add_Time_Windows.py and create busRun object for specified Run number,
	for all stops occurring at or after resched_init_time.

	RETURN: busRun object for specified Run.'''

      #subset based on matching Run number, and subset for stops only at or after resched_init_time
	data = data[(data["Run"] == Run) & data["ETA"] >= resched_init_time]
	data = data[data["ETA"] >= resched_init_time]

      # leave garage (beginning of route index), gas (end of route index)
      # get all rides between/including leave garage and gas indices.
	leave = rides[rides["Activity"]==4].index[0]
      gas = rides[rides["Activity"]==6].index[0]
      run = rides.iloc[leave:(gas+1)]

	class busRun:
        def __init__(self, BookingId, Run, Lats, Lons, PickupStart, PickupEnd, DropoffStart, DropoffEnd, spaceOn, mobAids):
            self.bookingId= BookingId
            self.run = Run
            self.Lats = Lats #list of Lats 
            self.Lons = Lons #list of Lons
            self.PickupStart = PickupStart #list of pickup window starting times
            self.PickupEnd = PickupEnd #list of pickup window ending times
            self.DropoffStart = DropoffStart #list of dropoff window starting times
            self.DropoffEnd = DropoffEnd #list of dropoff window ending times
            self.spaceOn = spaceOn #list of spaceOn things
            self.MobAids = MobAids #list of mobAids

      thisRun = busRun(run.BookingId, run.Run, run.LAT.tolist, run.LON.tolist, run.PickupStart.tolist, run.PickupEnd.tolist,
            run.DropoffStart.tolist, run.DropoffEnd.tolist, run.spaceOn.tolist, run.MobAids.tolist)

      return thisRun