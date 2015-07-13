def time_insertions(Run_Schedule, URID, pickUpDropOff = True):
	'''URID: of class URID, has bookingId, pickUpLocation, dropOffLocation, etc.
		Run_Schedule: Schedule of the run on which we're trying to insert the URID

		RETURN: table of inbound and outbound travel times between selected Run_Schedule points
		and URID pickup or dropoff location.'''

		if pickUpDropOff:
			Start = URID.PickupStart
			End = URID.PickupEnd
		if !pickupDropOff:
			Start = URID.DropoffStart
			End = URID.DropoffEnd

		windows = pd.DataFrame(columns = ["Node", "StartT", "EndT"], index = arange(0, Run_Schedule))


