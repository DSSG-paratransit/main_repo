import pandas as pd

def legPct(busRun, legTime=True, PctTime=True, 
                vector=False):
    '''
    busRun: a pandas dataframe for a single run schedule
        with columns [ETA,]
    legTime: if True, appends a new column with the time for each leg
    PctTime: if True, appends a new column describing the leg as pct of total run
    vector: if True, returns a vector describing leg as pct of total run
    return (default): A bus run with leg time and pct time columns
    '''
    # to correct for incorrect indexing from splicing data
    busRun.index = range(0, len(busRun))
    # print(len(busRun))

    totalTime = runTime(busRun['ETA'])
    
    # creates a vector with first index 0, other indexes
    # equal to the current ETA - the last ETA
    second = busRun.ETA.ix[1:]
    first = busRun.ETA.ix[:busRun.shape[0] - 2]
    second.index = range(0, len(second))
    timeVector = (second - first).tolist()
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

def runTime(busRun):
    '''
    busRun: pandas series with bus schedule
        with columns [ETA]
    returns the total time a bus spent out from base
    '''
    firstRow = busRun.iloc[0]
    lastRow = busRun.iloc[busRun.shape[0] - 1]

    # total time run takes
    return(lastRow - firstRow)

def main():
    data = pd.read_csv('../../data/UW_Trip_Data_14mo_QC.csv')

    # loop through unique pairs of dates/runs
    uniqueDR = data[['ServiceDate', 'Run']].drop_duplicates()
    print uniqueDR

    count = 0
    for row in uniqueDR.iterrows():
        count = count + 1
        print '\ncount: ' + str(count) + '\n'

        busRun = data[(data['ServiceDate'] == row[1].ServiceDate) & 
                 (data['Run'] == row[1].Run)]
        busRun = legPct(busRun)
        print(busRun[['Run', 'ETA', 'LegTime', 'PctOfRunTime']])

if __name__ == '__main__':
      main()