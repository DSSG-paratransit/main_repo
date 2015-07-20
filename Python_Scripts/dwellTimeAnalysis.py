import numpy as np
import os
import pandas as pd
import statsmodels.formula.api as smf
import sys

# @params: takes mobaid codes string
# @returns: list of mobaid strings
def splitCode(x):
	if type(x) is str:
		codes = x.split(',')
		return codes
	else:
		return []

# @returns binary T/F if string code is in string/list x
def containsCode(code, x):
	if code in x:
		return 1
	else:
		return 0

# @param: takes char to be repeated c and number of repeats n
# @returns: a string with c repeated n times
def characterString(c, n):
	r = ''
	for i in range(n):
		r = r + c
	return r

# to debug lambda functions
def test(x):
	print(x)

# get data file from 1st argument
data = None
try:
	data_path = os.path.join(os.pardir,'data',sys.argv[1])
	data = pd.read_csv(data_path)
except IOError:
	print('\n\tError: No file at ../data/' + sys.argv[1] + ' from ' + os.getcwd() + '\n')
	quit()
except IndexError: 
	print('\n\tdwellTimeAnalysis.py takes a csv file from\n\n\t\tmain_repo\data\n\n\tassuming that the file is run in the Python_Scripts folder\n')
	quit()

# gathers needed data
data.Activity = data.Activity.apply(lambda x: int(x))
# data = data.iloc(np.where((data.Activity == 0) | (data.Activity == 1)))
data = data[['ServiceDate','Run','ETA','DwellTime','Activity',
			'MobAids']].loc[(data.Activity == 0) | (data.Activity == 1)]
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

## combines boardings at the same stop
# temp = data # debug
# print(temp.columns.values) # debug
# temp.drop('MobAids', 1 ,inplace=True) # debug 
data = data.groupby(['ServiceDate','Run','ETA','DwellTime','Activity']).sum()
# 55-60 removes colums that have all 0 data
bool_column_df = data.apply(lambda x: (min(x) == 0) and (max(x) == 0))
bool_column_df.columns = ['values']
print(bool_column_df.values) # debug
columns = bool_column_df[bool_column_df.values].index.values
print(columns) # debug
data.drop(columns,1,inplace=True)
data.reset_index(inplace=True)
# print(data.columns.values) # debug
# print(data.equals(temp)) # debug

# splits data into boading and deboarding
boardings = data[data.Activity == 0]
# print(boardings) # debug
deboardings = data[data.Activity == 1]


###################################################################
# Need to check with Matthew                                      #
# -----------------------------                                   #
# is total dwell time for a stop is included for each client row? #
# or is total dwell time sum is divided among client rows?        #
###################################################################

# regression for boarding dwell times
x = ' + '.join(boardings.columns.values[6:])
y = 'DwellTime'
reg_formula = y + ' ~ ' + x
# print reg_formula # debug

# boarding regression
lmb = smf.ols(formula=reg_formula, data=boardings).fit() 
# deboarding regression
lmd = smf.ols(formula=reg_formula, data=deboardings).fit()

# prints and writes data to file
orig_stdout = sys.stdout
output = open("../data/dwell_time_mobaid_regression.txt", 'w')
sys.stdout = output
top = characterString('#', 78)  + '\n'
bottom = characterString('-', 78)
print top + characterString(' ', 34) + 'Boardings\n' + bottom
print lmb.summary()
print '\n\n' + top + characterString(' ', 33) + 'Deboardings\n' + bottom
print lmd.summary()
sys.stdout = orig_stdout
output.close()
