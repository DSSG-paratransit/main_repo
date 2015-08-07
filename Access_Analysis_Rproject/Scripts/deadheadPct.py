from legPct import legPct, runTime
import numpy as np
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
    print 'this should be 1: ' + str(sum(busRun.PctOfRunTime)) # debug
    deadheads = busRun[(busRun.TotalPass == 0)]
    return sum(deadheads.PctOfRunTime)

def deadheadVsCost(schedule):
    '''
    schedule: a full schedule 
    with columns [ServiceDate, Run, ETA, NumOn, TotalPass]
    '''
    uniqueDR = schedule[['ServiceDate', 'Run']].drop_duplicates()
    deadhead = []
    cost = []
    for row in uniqueDR.iterrows():
        busRun = schedule[(schedule['ServiceDate'] == row[1].ServiceDate) & 
                 (schedule['Run'] == row[1].Run)]
        print row[1].Run
        print row[1].ServiceDate

        totalPass = sum(busRun.NumOn)
        if totalPass > 0:
        # approximates average cost per boarding
            cost.append(float(runTime(busRun['ETA'])) / totalPass) 
            deadhead.append(deadheadPct(busRun[['ETA', 'TotalPass']]))
        else:
            print 'warning! run ' + str(row[1].Run) + ' on ' + str(row[1].ServiceDate) + ' has no passengers.'
    print cost
    print deadhead
    #plt.hist(deadhead)
    #plt.show()
    plt.plot(deadhead, cost, 'ro')
    plt.show()	

def main():
    data = pd.read_csv('../../data/UW_Trip_Data_14mo_QC.csv')
    #data.columns.values[24] = 'TotalPass'
    busRun = data[(data.Run == data.Run[0]) & (data.ServiceDate == data.ServiceDate[0])]    
    print str(deadheadPct(busRun)) + '\n'
    deadheadVsCost(data[['ServiceDate', 'Run', 'ETA', 'NumOn', 'TotalPass']])

if __name__ == '__main__':
      main()