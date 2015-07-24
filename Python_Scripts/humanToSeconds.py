import re

'''
@params: takes a string containing 24h time in HH:MM format 
@returns: the passed in value converted to seconds
'''
def humanToSeconds(hhmm):
	format = re.compile('\d\d:\d\d')
	if(format.match(hhmm) is None):
		raise ValueError('Time provided is in incorrect format')
	hoursAndSeconds = re.findall('\d\d', hhmm)
	# print(hoursAndSeconds[0]) # debug
	# print(hoursAndSeconds[1]) # debug
	return(int(hoursAndSeconds[0]) * 3600 + int(hoursAndSeconds[1]) * 60)

# For testing purposes
print(humanToSeconds(raw_input('Enter a 24h time in HH:MM format: ')))

