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
    with columns [ServiceDate, Run, ETA, NumOn, TotalPass]
    '''
    uniqueDR = schedule[['ServiceDate', 'Run']].drop_duplicates()
    toKeep = []
    print(uniqueDR)
    numOfRuns = len(uniqueDR)
    deadhead = []
    cost = []
    loopcount = 0

    # get deadhead pct for each Date/Run pair
    for row in uniqueDR.iterrows():
        busRun = schedule[(schedule['ServiceDate'] == row[1].ServiceDate) & 
                 (schedule['Run'] == row[1].Run)]

        totalPass = sum(busRun.NumOn)
        if totalPass > 0:
        # approximates average cost per boarding
            cost.append(float(runTime(busRun['ETA'])) / totalPass) 
            deadhead.append(deadheadPct(busRun[['ETA', 'TotalPass']]))
            toKeep.append(True)
        else:
            print 'warning! run ' + str(row[1].Run) + ' on ' + str(row[1].ServiceDate) + ' has no passengers.'
            toKeep.append(False)
        
        loopcount = loopcount + 1
        os.system(['clear', 'cls'][os.name == 'nt'])
        print row[1].Run
        print row[1].ServiceDate
        print str(float(loopcount)/numOfRuns * 100) + '%' + ' done\n'

    print cost
    print deadhead

    # remove rows with bad data
    uniqueDR[toKeep]

    # write results to file
    cost = np.asarray(cost)
    deadhead = np.asarray(deadhead)
    uniqueDR['CostProxy'] = cost
    uniqueDR['PctDeadhead'] = deadhead
    # IMPORTANT: change file name if not 4mo
    uniqueDR.to_csv('../../data/4mo_deadhead_results.csv')

    # regressions
    results = smf.ols('cost ~ deadhead', data=uniqueDR).fit()
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
    data = pd.read_csv('../../data/UW_Trip_Data_14mo_QC.csv')
    #data.columns.values[24] = 'TotalPass'
    busRun = data[(data.Run == data.Run[0]) & (data.ServiceDate == data.ServiceDate[0])]    
    print str(deadheadPct(busRun)) + '\n'
    deadheadVsCost(data[['ServiceDate', 'Run', 'ETA', 'NumOn', 'TotalPass']])
    #[data.ServiceDate == data.ServiceDate[0]] ^insert this before the [ for a single day

if __name__ == '__main__':
      main()