from isMonth import isMonth
from legPct import legPct, runTime
import numpy as np
import multiprocessing as mp
import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import re

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

def getSingleDC(row, schedule,results,pnum):
    output = []
    busRun = schedule[(schedule['ServiceDate'] == row[1].ServiceDate) & 
             (schedule['Run'] == row[1].Run)]
    totalPass = sum(busRun.NumOn)
    if 8 in busRun.Activity.unique():
        output = [row[1].ServiceDate, row[1].Run, False, True, None, None]
    elif totalPass <= 0:
        output = [row[1].ServiceDate, row[1].Run, False, False, None, None]
    else: 
        time = float(runTime(busRun['ETA']))
        if time < 14400: # 4 hours
            time = 14400.0
        cost = time / totalPass
        deadhead = deadheadPct(busRun[['ETA', 'TotalPass']])
        output = [row[1].ServiceDate, row[1].Run, True, False, deadhead, cost]
    results[pnum] = output

def deadheadVsCost(schedule):
    '''
    schedule: a full schedule 
    with columns [ServiceDate, Run, Activity, ETA, NumOn, TotalPass,]
    '''
    uniqueDR = schedule[['ServiceDate', 'Run']].drop_duplicates()
    manager = mp.Manager()
    results = manager.dict()
    procs = []
    pnum = 0
    for row in uniqueDR.iterrows():
        p = mp.Process(target=getSingleDC, args=(row,schedule,results,pnum,))
        procs.append(p)
        p.start()
        pnum = pnum + 1
    for proc in procs:
        proc.join()
    print(results.values())
    results = pd.DataFrame(results.values())

    print(results)

    # write results to file
    # cost = np.asarray(cost)
    # deadhead = np.asarray(deadhead)
    # uniqueDR['CostProxy'] = cost
    # uniqueDR['PctDeadhead'] = deadhead
    # # IMPORTANT: change file name if not 4mo
    # uniqueDR.to_csv('../../data/4mo_deadhead_cost_nptest.csv', index=False)

    # # regressions
    # results = smf.ols('cost ~ deadhead', data=uniqueDR).fit()
    # print results.summary()
    # results = smf.ols('np.log(cost) ~ deadhead', data=uniqueDR).fit()
    # print results.summary()

    # plots
    # plt.hist(deadhead)
    # plt.savefig('../output/deadheadHist.png')
    # plt.close()
    # plt.plot(deadhead, cost, 'ro')
    # plt.xlabel('Percent Deadhead')
    # plt.ylabel('Length of Trip / Number of passengers (seconds)')
    # plt.savefig('../output/figure.png')
    # plt.close()


def main():
    data = pd.read_csv('../../data/UW_Trip_Data_4mo_QC_capacity.csv')
    #data.columns.values[24] = 'TotalPass'
    busRun = data[(data.Run == data.Run[0]) & (data.ServiceDate == data.ServiceDate[0])]    
    print str(deadheadPct(busRun)) + '\n'
    deadheadVsCost(data[date.match(data.ServiceDate)][['ServiceDate', 'Run', 'Activity', 'ETA', 'NumOn', 'TotalPass']])
    #[data.ServiceDate == '0015-04-13'] ^insert this before the [ for a single day

if __name__ == '__main__':
      main()