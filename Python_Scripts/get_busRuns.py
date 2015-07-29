def get_busRuns(data, Run, URID):
      ''' take pd.DataFrame from add_Time_Windows.py and create busRun object for specified Run number,
      for all scheduled stops for the day, between activity code 4 and the first of either 6, 16, or 3.

      RETURN: busRun pandas.dataframe for specified Run.'''


      # leave garage (beginning of route index), gas (end of route index)
      # get all rides between/including leave garage and gas indices.
      print("Testing get_busRuns on run " + Run)

      # ISSUE: CUTTING OFF BUS STOPS PREMATURELY AT resched_init_time!!!!
      dataSub = data[(data["Run"] == Run)]

      # if full busRun or partial
      if URID is None:
            #subset only the rides that aren't 6, 16, or 3:
            leave = dataSub.index.min()
      else:
            leave = dataSub.loc[(dataSub['LAT'] == URID.LAT) 
                  & (dataSub['LON'] == URID.LON) & (dataSub['ClientId'] == URID.ClientId)]

      gas = dataSub[(dataSub["Activity"]==6)|(dataSub["Activity"]==16)|(dataSub["Activity"]==3)].index.min()
      busRun = dataSub.iloc[leave:gas]

      return busRun



### TEST THIS FUNCTION:
def main():
      import pandas as pd
      import numpy as np
      from get_URIDs import get_URIDs
      from add_TimeWindows import add_TimeWindows

      data_filepath = "../data/single_clean_day.csv"
      data_allday = pd.read_csv(data_filepath, header = True) #import one day's QC'ed data
      windowsz = 30*60 #Variable window size, in seconds

      newdata = add_TimeWindows(data_allday, windowsz)
      Bus = newdata.Run.iloc[50]
      busRun = get_busRuns(newdata, Bus, None)

if __name__ == '__main__':
      main()