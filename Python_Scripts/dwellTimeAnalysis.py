import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

def splitCode(x):
	if type(x) is str:
		codes = x.split(',')
		return codes
	else:
		return []

def containsCode(code, x):
	if code in x:
		return 1
	else:
		return 0

def characterString(c, n):
	r = ''
	for i in range(n):
		r = r + c
	return r

data = pd.read_csv('D:\\Documents\\Repos\\main_repo\\data\\single_clean_day.csv')

# gathers needed data
data = data[['ServiceDate','Run','ETA','DwellTime','PassOn','PassOff','MobAids']]
allCodes = ['A','AM','AP','AR','BB','CA','CB','CI','CS','CT','H','H1','H2','HD','LI',
			'MO','N','NR','OR','OX','PEL','PK','SA','SC','ST','SVC','U','V','V1','V2',
			'WA','WG','WH','WK','WT','WX','0T']
data.MobAids = data.MobAids.apply(lambda x: splitCode(x))

# creates a column with binary values for each code
for code in allCodes:
	data[code] = data.MobAids.apply(lambda x: containsCode(code, x))
# print(data) # debug

# Attempt to fix an error caused in the regression by this 0T
data.rename(columns={'0T' : 'OT'}, inplace=True)

boardings = data[pd.notnull(data.PassOn)]
# print(boardings) # debug
deboardings = data[pd.isnull(data.PassOn)]


###################################################################
# Need to check with Matthew                                      #
# -----------------------------                                   #
# is total dwell time for a stop is included for each client row? #
# or is total dwell time sum is divided among client rows?        #
###################################################################

# regression for boarding dwell times
x = ' + '.join(boardings.columns.values[7:])
y = 'DwellTime'
reg_formula = y + ' ~ ' + x
# print reg_formula # debug

# boarding regression
lmb = smf.ols(formula=reg_formula, data=boardings).fit() 
# deboarding regression
lmd = smf.ols(formula=reg_formula, data=deboardings).fit()

top = characterString('#', 78)  + '\n'
bottom = characterString('-', 78)
print top + characterString(' ', 34) + 'Boardings\n' + bottom
print lmb.summary()
print '\n\n' + top + characterString(' ', 33) + 'Deboardings\n' + bottom
print lmd.summary()
