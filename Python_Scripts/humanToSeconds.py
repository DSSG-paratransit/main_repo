import re

'''
@params: takes a string containing 24h time in HH:MM format 
@returns: the passed in value converted to seconds
'''
def humanToSeconds(hhmm):

	# Invalid format
	format = re.compile('\d\d:\d\d')
	if(format.match(hhmm) is None):
		raise ValueError('Time provided is in incorrect format')
	
	hoursAndSeconds = re.findall('\d\d', hhmm)
	# print(hoursAndSeconds[0]) # debug
	# print(hoursAndSeconds[1]) # debug

	hour = int(hoursAndSeconds[0])
	sec = int(hoursAndSeconds[1])

	# Invalid Time
	if(hour > 24 or sec > 59):
		raise ValueError('Time provided is invalid')

	return(hour * 3600 + sec * 60)

# For testing purposes
print(humanToSeconds(raw_input('Enter a 24h time in HH:MM format: ')))

