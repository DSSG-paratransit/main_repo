import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#must flag OT passengers at some point! 

def passenger_sum(thesum, iter):

    """
    Function to be used with reduce in passenger_count_at_checkpoint

 
    Args:
    thesum (int): param to hold passenger sum for reduce 
    iter (int): on/off passenger counts that we are iterating over (i.e. SpaceOn
    or SpaceOff for WC or AM capacity)

    Returns:
    Sum of thesum and iter (i.e. total passenger count at given time step)
    
    """
    
    if pd.isnull(iter):
        return thesum
    passenger_count = iter

    return thesum + passenger_count

class PassengerCounter():

    """ 
    Class to implement the calculation for both ambulatory and wheelchair 
    capacity from start time to a given "checkpoint," i.e. end of run.

    Attributes:
    on (array): column from df that has entries for WC/AM numbers at each time step 
    off (array): column from df that has entries for WC/AM numbers at each time step 
    
    """
    
    def __init__(self, on, off):

        """
        
        Args: 
        on (array): column from df that has entries for WC/AM numbers at each time step 
        off (array): column from df that has entries for WC/AM numbers at each time step 
        
        """
        self.on = on
        self.off = off

    def passenger_count_at_checkpoint(self, checkpoint):

        """
        
        Args:
        checkpoint (int): index of each timestep at which passenger(s) get on/off bus 

        Returns:
        Difference between passengers getting on and off bus at given checkpoint (timestep) 

        """
        on_count = reduce(passenger_sum, self.on[:checkpoint],0)
        off_count = reduce(passenger_sum, self.off[:checkpoint],0)
    
        
        return on_count - off_count

    def transactions_at_checkpoint(self, checkpoint):

        """
        Ultimately want a method that checks that on capacity = off capacity for given clientId.
        
        Args: 

        Returns: 

        """
        on_transaction = self.on[checkpoint]
        off_transaction = self.off[checkpoint]

        #return "on: %s, off: %s" % (on_transaction, off_transaction)

def addCapacityColumn(dataframe,busDateCol=False):

    """
    
    Args:
    dataframe (string): path to filename from which to create our dataframe
    busDateCol (bool): default False, make True if the dataframe includes different service dates as well as bus runs

    Returns:
    original dataframe with WC and AM columns added 

    """

    df = pd.DataFrame.from_csv(dataframe, header=0, sep=',')
    df = df.set_index('Run')
    no_shows = np.where(df['SchedStatus'] != 1.)
    df['SpaceOn'].iloc[no_shows] = np.NAN
    df['SpaceOff'].iloc[no_shows] = np.NAN

    df['wcOn'], df['wcOff'] = createOnOffcols(dataframe, 'SpaceOn', 'SpaceOff')
    df['amOn'], df['amOff'] = createOnOffcols(dataframe, 'SpaceOn', 'SpaceOff', wc=False)
    df['wcCapacity'] = ""
    df['amCapacity'] = ""
    
    
    if busDateCol:
        zipped = np.unique(zip(df['ServiceDate'],df.index))
        for i in range(len(zipped)):
            this_run = df[(df.index == zipped[i][1]) & (df['ServiceDate'] == zipped[i][0])]
            on_wc = np.array(this_run['wcOn'])
            off_wc = np.array(this_run['wcOff'])
            p_wc = PassengerCounter(on_wc,off_wc)
            on_am = np.array(this_run['amOn'])
            off_am = np.array(this_run['amOff'])
            p_am = PassengerCounter(on_am, off_am)
            df['wcCapacity'].loc[str(run)] = [p_wc.passenger_count_at_checkpoint(i) for i in range(1,len(on_wc)+1)]
            df['amCapacity'].loc[str(run)] = [p_am.passenger_count_at_checkpoint(i) for i in range(1,len(on_am)+1)]

    if not busDateCol:
        for run in np.unique(df.index):
            print type(run)
            this_run = df[(df.index == run)]
            on_wc = np.array(this_run['wcOn'])
            off_wc = np.array(this_run['wcOff'])
            p_wc = PassengerCounter(on_wc,off_wc)
            on_am = np.array(this_run['amOn'])
            off_am = np.array(this_run['amOff'])
            p_am = PassengerCounter(on_am, off_am)
            df['wcCapacity'].loc[str(run)] = [p_wc.passenger_count_at_checkpoint(i) for i in range(1,len(on_wc)+1)]
            df['amCapacity'].loc[str(run)] = [p_am.passenger_count_at_checkpoint(i) for i in range(1,len(on_am)+1)]
            
    df.to_csv('tmp_wpass.csv', sep=',')
    

            
def createOnOffcols(dataframe, onstring, offstring, wc=True):

    """
    
    Args:
    dataframe (string): path to filename from which to create our dataframe
    onstring (string): column header name for "on" data, i.e. "SpaceOn"
    offstring (string): column header name for "off" data, i.e. "SpaceOff"
    wc (bool): default True

    Returns:
    two arrays that are on and off columns, respectively 

    """

    df = pd.DataFrame.from_csv(dataframe, header=0, sep=',')
    df = df.set_index('Run')
    no_shows = np.where(df['SchedStatus'] != 1.)
    df[onstring].iloc[no_shows] = np.NAN
    df[offstring].iloc[no_shows] = np.NAN

    if wc:
        allcols_On = [df[onstring].str.split(",",expand=True)[i].str.extract('(?P<letter>WG|WH|PK|WX|SC|OR)(?P<digit>\d)') for i in range(df[onstring].str.split(",",expand=True).shape[1])]
        allcols_Off = [df[offstring].str.split(",",expand=True)[i].str.extract('(?P<letter>WG|WH|PK|WX|SC|OR)(?P<digit>\d)') for i in range(df[offstring].str.split(",",expand=True).shape[1])]
    else:
        allcols_On = [df[onstring].str.split(",",expand=True)[i].str.extract('(?P<letter>AM)(?P<digit>\d)') for i in range(df[onstring].str.split(",",expand=True).shape[1])]
        allcols_Off = [df[offstring].str.split(",",expand=True)[i].str.extract('(?P<letter>AM)(?P<digit>\d)') for i in range(df[offstring].str.split(",",expand=True).shape[1])]


    for i in range(len(allcols_On)):
        allcols_On[i].digit[pd.isnull(allcols_On[i].digit)] = 0
        allcols_On[i].digit[~pd.isnull(allcols_On[i].digit)] = [int(j) for j in allcols_On[i].digit[~pd.isnull(allcols_On[i].digit)]] 
        allcols_Off[i].digit[pd.isnull(allcols_Off[i].digit)] = 0
        allcols_Off[i].digit[~pd.isnull(allcols_Off[i].digit)] = [int(j) for j in allcols_Off[i].digit[~pd.isnull(allcols_Off[i].digit)]]

  
    return sum([allcols_On[i].digit for i in range(len(allcols_On))]), sum([allcols_Off[i].digit for i in range(len(allcols_Off))])



def checkCapacityInsertPt(URID, busRun):
    """

    Args:

    Returns:

    """
