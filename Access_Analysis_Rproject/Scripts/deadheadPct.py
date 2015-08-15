from legPct import legPct, runTime
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

def deadheadPct(busRun):
    '''
    busRun: a single bus run schedule 
    	with columns [ETA, TotalPass]
    returns: a float percent
    '''
    busRun = legPct(busRun)
    # print 'this should be 1: ' + str(sum(busRun.PctOfRunTime)) # debug
    deadheads = busRun[(busRun.TotalPass == 0)]
    return sum(deadheads.PctOfRunTime)

def deadheadVsCost(schedule):
    '''
    schedule: a full schedule 
    with columns [ServiceDate, Run, Activity, ETA, NumOn, TotalPass,]
    '''
    uniqueDR = schedule[['ServiceDate', 'Run']].drop_duplicates()
    toKeep = []
    print(uniqueDR)
    numOfRuns = len(uniqueDR)
    deadhead = []
    cost = []
    breakdownDate = []
    breakdownRun = []
    loopcount = 0
    numDropped = 0

    # get deadhead pct for each Date/Run pair
    for row in uniqueDR.iterrows():
        busRun = schedule[(schedule['ServiceDate'] == row[1].ServiceDate) & 
                 (schedule['Run'] == row[1].Run)]

        totalPass = sum(busRun.NumOn)
        if 8 in busRun.Activity.unique():
            print 'warning! run ' + str(row[1].Run) + ' on ' + str(row[1].ServiceDate) + ' breaks down.'
            toKeep.append(False)
            breakdownRun.append(row[1].Run)
            breakdownDate.append(row[1].ServiceDate)
        elif totalPass > 0:
        # approximates average cost per boarding
            time = float(runTime(busRun['ETA']))
            if time < 14400: # 4 hours
                time = 14400.0
            icost = time / totalPass
            cost.append(icost) 
            deadhead.append(deadheadPct(busRun[['ETA', 'TotalPass']]))
            toKeep.append(True)
        else:
            print 'warning! run ' + str(row[1].Run) + ' on ' + str(row[1].ServiceDate) + ' has no passengers.'
            toKeep.append(False)
            numDropped = numDropped + 1
        
        loopcount = loopcount + 1
        os.system(['clear', 'cls'][os.name == 'nt'])
        print row[1].Run
        print row[1].ServiceDate
        print str(float(loopcount)/numOfRuns * 100) + '%' + ' done\n'

    print cost
    print deadhead
    print('')
    print('Number "dropped": ' + str(numDropped))
    uniqueDRLen = len(uniqueDR) 
    print('Number needed: ' + str(uniqueDRLen - len(cost)))
    if False in toKeep:
        print('Drop in toKeep found.')

    # remove rows with bad data
    uniqueDR = uniqueDR[toKeep]
    print('Number dropped: ' + str(uniqueDRLen - len(uniqueDR)))

    # write breakdowns to file
    #pd.DataFrame({'ServiceDate' : breakdownDate,
                 #'Run' : breakdownRun}).to_csv('../../data/4mo_broken_buses.csv')

    # write results to file
    cost = np.asarray(cost)
    deadhead = np.asarray(deadhead)
    uniqueDR['CostProxy'] = cost
    uniqueDR['PctDeadhead'] = deadhead
    # IMPORTANT: change file name if not 4mo
    uniqueDR.to_csv('../../data/4mo_deadhead_cost_adjusted_results.csv', index=False)

    # regressions
    results = smf.ols('cost ~ deadhead', data=uniqueDR).fit()
    print results.summary()
    results = smf.ols('np.log(cost) ~ deadhead', data=uniqueDR).fit()
    print results.summary()

    # plots
    plt.hist(deadhead)
    plt.savefig('../output/deadheadHist.png')
    plt.close()
    plt.plot(deadhead, cost, 'ro')
    plt.xlabel('Percent Deadhead')
    plt.ylabel('Length of Trip / Number of passengers (seconds)')
    plt.savefig('../output/figure.png')
    plt.close()


def main():
    data = pd.read_csv('../../data/UW_Trip_Data_4mo_QC_capacity.csv')
    #data.columns.values[24] = 'TotalPass'
    busRun = data[(data.Run == data.Run[0]) & (data.ServiceDate == data.ServiceDate[0])]    
    print str(deadheadPct(busRun)) + '\n'
    deadheadVsCost(data[['ServiceDate', 'Run', 'Activity', 'ETA', 'NumOn', 'TotalPass']])
    #[data.ServiceDate == '0015-04-13'] ^insert this before the [ for a single day

if __name__ == '__main__':
      main()