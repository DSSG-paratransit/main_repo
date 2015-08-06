import pandas as pd

def deadheadPct(busRun, legTime=True, PctTime=True, 
                vector=False):
    # to correct for incorrect indexing from splicing data
    busRun.index = range(0, len(busRun))
    print(len(busRun))
    
    firstRow = busRun.iloc[0]
    lastRow = busRun.iloc[busRun.shape[0] - 1]

    # total time run takes
    totalTime = lastRow.ETA - firstRow.ETA
    
    # creates a vector with first index 0, other indexes
    # equal to the current ETA - the last ETA
    second = busRun.ix[1:]
    first = busRun.ix[:busRun.shape[0] - 1]
    second.index = range(0, len(second))
    timeVector = (second.ETA - first.ETA).tolist()
    timeVector.pop()
    timeVector = [0] + timeVector

    # the percent of the run that the individual leg took
    pctTimeTaken = timeVector / totalTime

    if vector:
        return(pctTimeTaken)

    # add columns to dataframe
    if legTime:
        busRun['LegTime'] = timeVector
    if PctTime:
        busRun['PctOfRunTime'] = pctTimeTaken

    return(busRun)

def main():
    data = pd.read_csv('../../data/UW_Trip_Data_14mo_QC.csv')

    # loop through unique pairs of dates/runs
    uniqueDR = data[['ServiceDate', 'Run']].drop_duplicates()
    for row in uniqueDR.iterrows():
        busRun = data[(data['ServiceDate'] == row[1].ServiceDate) & 
                 (data['Run'] == row[1].Run)]
        busRun = deadheadPct(busRun)
        print(busRun[['Run', 'ETA', 'LegTime', 'PctOfRunTime']])

if __name__ == '__main__':
      main()