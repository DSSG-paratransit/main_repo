import re

def humanToSeconds(hhmm):
	'''
	@params: takes a string containing 24h time in HH:MM format
		throws ValueError if time is the wrong format
	@returns: the passed in value converted to seconds
	'''

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

def secondsToHuman(totalSeconds):
	'''
	@params: takes totalSeconds as an int
		throws ValueError if totalSeconds >= 86400 or <0
	@returns: a string with time in 24h HH:MM format 
	'''

	if (totalSeconds >= 86400) or (totalSeconds < 0):
		raise ValueError('Seconds provided is out of bounds (the number of seconds in a day)')

	hours = str(totalSeconds / 3600)
	minutes = str(int(round(totalSeconds % 3600 / float(60))))

	def fixFormat(component):
		format = re.compile('\d\d')
		if format.match(component) is None:
			return('0' + component)
		return component

	return(fixFormat(hours) + ':' + fixFormat(minutes))

def secondsFactorization(seconds):
	'''
	param: a positive number of seconds (else ValueError)
	returns: list [h,m,s]
	'''
	if seconds < 0:
		raise ValueError('not a non negative number')
	return([seconds / 3600, seconds % 3600 / 60, seconds % 60])
	
def main():
	import sys
	option = None
	try:
		option = sys.argv[1]
	except IndexError:
		print(humanToSeconds(raw_input('Enter a 24h time in HH:MM format: ')))
		print(secondsToHuman(input('Enter a number of seconds to convert to 24h time: ')))
		print(secondsFactorization(input('Enter a positive number of seconds: ')))

	while (option == '1') or (option == '2') or (option == '3'):
		if option == '1':
			print(humanToSeconds(raw_input('Enter a 24h time in HH:MM format: ')))
		elif option == '2':
			print(secondsToHuman(input('Enter a number of seconds to convert to 24h time: ')))
		elif option == '3':
			print(secondsFactorization(input('Enter a positive number of seconds: ')))
		option = raw_input('\nagain? ')
		print('')


if __name__ == '__main__':
	main()

