def isMonth(month, year, date):
	'''
	month: (int)
	year: the year (int)
	date: string yyyy-mm-dd
	'''
	import re

	year = str(year)
	if len(year) == 2:
		year = '00' + year
	month = str(month)
	if len(month) == 1:
		month = '0' + month

	# print date
	# print month
	# print year

	regex = re.compile(year + '-' + month + '-\d\d') 
	if regex.match(str(date)) is None:
		# print 'False + \n'
		return False
	# print 'True + \n'
	return True

