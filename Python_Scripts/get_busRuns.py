def get_busRuns(data, Run, URID, resched_init_time):
      ''' take pd.DataFrame from add_Time_Windows.py and create busRun object for specified Run number,
      for all scheduled stops for the day, between activity code 4 and the first of either 6, 16, or 3.
      RETURN: busRun pandas.dataframe for specified Run.'''


      # leave garage (beginning of route index), gas (end of route index)
      # get all rides between/including leave garage and gas indices.
      print("Testing get_busRuns on run " + Run)

      dataSub = data[(data["Run"] == Run) & data['ETA'] >= resched_init_time]

      # if full busRun or partial
      if URID is None:
            #subset only the rides that aren't 6, 16, or 3:
            leaveIndex = dataSub.index.min()
      else:
            leave = dataSub.loc[(dataSub['LAT'] == URID.PickUpCoords.LAT) 
                  & (dataSub['LON'] == URID.PickUpCoords.LON) 
                  & (dataSub['BookingId'] == URID.BookingId)]
            leaveIndex = leave.index.min()

      baseIndex = dataSub[(dataSub["Activity"]==6)|(dataSub["Activity"]==16)|(dataSub["Activity"]==3)].index.min()
      busRun = dataSub.iloc[leaveIndex:baseIndex]

      return busRun



### TEST THIS FUNCTION:
def main():
      import pandas as pd
      import numpy as np
      from get_URIDs import get_URIDs
      from add_TimeWindows import add_TimeWindows

      data_filepath = "../data/single_day_TimeWindows.csv"
      data_allday = pd.read_csv(data_filepath) #import one day's QC'ed data
      # print(data_allday)

      windowsz = 30*60 #Variable window size, in seconds
      
      # newdata = add_TimeWindows(data_allday, windowsz)
      # Bus = newdata.Run.iloc[50]

      bus = '680SEB'
      busRun = get_busRuns(data_allday , bus, get_URIDs(data_allday, bus, 53684)[1])
      print busRun

if __name__ == '__main__':
      main()