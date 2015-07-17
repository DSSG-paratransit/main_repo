def get_busRuns(data, Run, resched_init_time):
	''' take pd.DataFrame from add_Time_Windows.py and create busRun object for specified Run number,
	for all stops occurring at or after resched_init_time.

	RETURN: busRun pandas.dataframe for specified Run.'''

      #subset based on matching Run number, and subset for stops only at or after resched_init_time
	dataSub = data[(data["Run"] == Run) & (data["ETA"] >= resched_init_time)]

      # leave garage (beginning of route index), gas (end of route index)
      # get all rides between/including leave garage and gas indices.
	print("Testing get_busRuns on run %s" % bus_Run)

      # ISSUE: CUTTING OFF BUS STOPS PREMATURELY AT resched_init_time!!!!
      dataSub = data[(data["Run"] == bus_Run) & (data["ETA"] >= resched_init_time)]


      #subset only the rides that aren't 6, 16, or 3:
      leave = dataSub.index.min()
      gas = dataSub[(dataSub["Activity"]==6)|(dataSub["Activity"]==16)|(dataSub["Activity"]==3)].index.min()
      busRun = dataSub.iloc[leave:(gas+1)]

      return busRun





### TEST THIS FUNCTION:
#import pandas as pd
#import numpy as np

#data_filepath = "/Users/fineiskid/Desktop/Access_Analysis_Rproject_local/data/single_clean_day.csv"
#data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
#windowsz = 30*60 #Variable window size, in seconds

#newdata = add_TimeWindows(data_allday, windowsz)
#Bus = newdata.Run.iloc[50]
#busRun = get_busRuns(newdata, Bus, 0)