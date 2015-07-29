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

        if on_count - off_count < 0.:
            return np.nan
    
        
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



def checkCapacityInsertPts(URID, busRun):
    """
    Assumes that busRun df has wcCapacity, amCapacity columns, and that URID
    has amOn/Off and wcOn/Off columns added. First check most restrictive window,
    if this is not okay then return null values. next check max in windows between
    PUStart & PUEnd and DOStart & DOEnd. If these are okay then return the URID as is.
    If either of these other windows are NOT okay  then we need to check in a more 
    granular way to see what are new time windows are. Ultimately the URID should 
    return the new time windows, so the  class will need to be changed to include 
    something like self.PickupInsert, self.DropoffInsert, which will be the start/end
    for new windows (or same if old windows work, or null if capacity is not okay). 

    Args:

    Returns:

    """

    def amCapacity(wcCapacityTotal):
        '''
        Quick function to do something 
        like switch statements in python.
        
        Args: 
        wcCapacityTotal (string): str(max_wcCapacity + URID.wcOn), basically total wc capacity 
        given max wc capacity in that time window and URID wc capacity in string form 
        
        Returns:
        appropriate am capacity given this total wc capacity, else -1000 if wc capacity entered is not in 
        dictionary. need to catch cases where wc capacity is over 3 but am capacity is otherwise acceptably low 
        
        '''
        return {
            '0': 12,
            '1': 8,
            '2': 4,
            '3': 0,
            }.get(wcCapacityTotal,-1000)

    restrictive_window = np.where((busRun['ETA'] > URID.PickupEnd ) & (busRun['ETA'] < URID.DropoffStart))
    PickupWindow = np.where((busRun['ETA'] > URID.PickupStart) & (busRun['ETA'] < URID.PickupEnd))
    DropoffWindow = np.where((busRun['ETA'] > URID.DropoffStart) & (busRun['ETA'] < URID.DropoffEnd))

    max_wcCapacity = np.max(busRun['wcCapacity'].iloc[restrictive_window])
    max_amCapacity = np.max(busRun['amCapacity'].iloc[restrictive_window])
    full = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.wcOn > amCapacity(str(max_wcCapacity + URID.wcOn)))
    if full:
        return URID.PickupInsert, URID.DropoffInsert = np.nan, np.nan
    elif not full:
        max_wcCapacity_pickup = np.max(busRun['wcCapacity'].iloc[PickupWindow])
        max_amCapacity_pickup = np.max(busRun['amCapacity'].iloc[PickupWindow])
        full_pickup = (max_wcCapacity_pickup + URID.wcOn > 3) & (max_amCapacity_pickup + URID.amOn > amCapacity(str(max_wcCapacity_pickup + URID.wcOn)))
        if full_pickup:
            full_indx = (busRun['wcCapacity'].iloc[DropoffWindow] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[DropoffWindow] + URID.amOn > amCapacity(str(max_wcCapacity_dropoff + URID.wcOn)))
            # how do we get the next index after the one where capacity is maximum? how do we pick off cases
            # where max is not unique? 
            next_full_pickup = (busRun['wcCapacity'].iloc[PickupWindow].loc[full_indx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[PickupWindow].loc[full_indx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[PickupWindow].loc[full_indx] + URID.wcOn)))
            if next_full_pickup:
                # repeat for next indice
            elif not next_full_pickup:
                URID.PickupInsert = busRun['ETA'].iloc[PickupWindow].loc[full_indx] # actually should be next closest time
        max_wcCapacity_dropoff = np.max(busRun['wcCapacity'].iloc[DropoffWindow])
        max_amCapacity_dropoff = np.max(busRun['amCapacity'].iloc[DropoffWindow])
        full_dropoff = (max_wcCapacity_dropoff + URID.wcOn > 3) & (max_amCapacity_dropoff + URID.amOn > amCapacity(str(max_wcCapacity_dropoff + URID.wcOn)))
        if full_dropoff:
            full_indx = (busRun['wcCapacity'].iloc[DropoffWindow] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[DropoffWindow] + URID.amOn > amCapacity(str(max_wcCapacity_dropoff + URID.wcOn)))
            # how do we get the next index after the one where capacity is maximum? how do we pick off cases
            # where max is not unique? 
            next_full_dropoff = (busRun['wcCapacity'].iloc[DropoffWindow].loc[full_indx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[DropoffWindow].loc[full_indx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[DropoffWindow].loc[full_indx] + URID.wcOn)))
            if next_full_dropoff:
                # repeat for next indice
            elif not next_full_dropoff:
                URID.DropoffInsert = busRun['ETA'].iloc[DropoffWindow].loc[full_indx] # actually should be next closest time
    

       
        
        
