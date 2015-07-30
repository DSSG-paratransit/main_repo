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
    has amOn/Off and wcOn/Off columns added so it can return capacity insert points. 
    
    **Currently not implemented: apparently 2 WC + PK + AM is allowed (how often does 
    this occur in 18 month data?), so we need a check for this. Perhaps make PK 
    count as 0.9xWC?**

    Args:

    Returns:
    URID.PickupInsert, URID.DropoffInsert

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



    def checkWindow(URID, busRun, window, dropoffpickupiloc, dropoffpickupindx):

    '''
    Check max capacity + URID capacity in windows between
    PUStart & PUEnd or DOStart & DOEnd. If these are okay then return insert points 
    as PUStart and DOEnd. If either of these other windows are NOT okay  
    then look at timestep right after (pickup) or right before (dropoff) where
    max capacity occurs. Repeat if still full. 
    
    **Currently not implemented: check on
    the edge case, i.e. looking between end of time window and PUEnd or DOStart and 
    last checked time window. The returned value in these cases is just beginning or 
    end of time window itself.**
    
    Args: 
    busRun (dataframe): contains all info for bus run to check 
    URID (class instance): contains all info for unscheduled request 
    window (array): window in which to check capacity, i.e. PickupWindow/DropoffWindow
    dropoffpickupiloc (int): used for indexing window array. For pickups we want closest to PickupEnd, i.e. + 1. For dropoffs we want closest to DropoffStart, i.e. -1.
    dropoffpickupindx (int): used for indexing bool array in the event of non-unique max capacity. For pickups
    we want closest to PickupEnd, i.e. -1. For dropoffs we want closest to DropoffStart, i.e. 0.

    Returns:
    URID.PickupInsert or URID.DropoffInsert depending on how it's called 
    

    '''
    max_wcCapacity = np.max(busRun['wcCapacity'].iloc[window])
    max_amCapacity = np.max(busRun['amCapacity'].iloc[window])
    full_bool = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.amOn > amCapacity(str(max_wcCapacity + URID.wcOn)))
    
    if full_bool:
        full_indx = np.array((busRun['wcCapacity'].iloc[window] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window] + URID.amOn > amCapacity(str(max_wcCapacity + URID.wcOn))))
                        
        # check capacity in window if max capacity is unique   
        if len(busRun['wcCapacity'].iloc[window].loc[full_indx]) == 1:
            next_full_bool = np.array((busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn))))
            if next_full_bool:
                counter = pickupdropoffiloc
                if pickupdropoffiloc == 1:
                    while busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] < busRun['ETA'].iloc[window[-1]]:
                        counter += 1
                        check_full_bools = np.array((busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                        if check_full_bools:
                            continue
                        elif check_full_bools & (busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] == busRun['ETA'].iloc[window[-1]]):
                            return busRun['ETA'].iloc[window[-1]]
                        elif not check_full_bools:
                            return busRun['ETA'].iloc[window + counter].loc[full_indx]
                elif pickupdropoffiloc == -1:
                    while busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] > busRun['ETA'].iloc[window[0]]:
                        counter -= 1
                        check_full_bools = np.array((busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                        if check_full_bools:
                            continue
                        elif check_full_bools & (busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] == busRun['ETA'].iloc[window[0]]):
                            return busRun['ETA'].iloc[window[0]]
                        elif not check_full_bools:
                            return busRun['ETA'].iloc[window + counter].loc[full_indx]
            elif not next_full_bool:
                    return busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx]

        # if there are multiple places in PickupWindow where we go over max capacity
        # choose one that is closest to PickupEnd
        elif len(busRun['wcCapacity'].iloc[window].loc[full_indx]) > 1:
                next_full_bool = np.array((busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                if next_full_bool:
                    counter = pickupdropoffiloc
                    if pickupdropoffiloc == 1:
                        while busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] < busRun['ETA'].iloc[window[-1]]:
                            counter += 1
                            check_full_bools = np.array((busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] == busRun['ETA'].iloc[window[-1]]):
                                return busRun['ETA'].iloc[window[-1]]
                            elif not check_full_bools:
                                return busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]
                    if pickupdropoffiloc == -1:
                        while busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] > busRun['ETA'].iloc[window[0]]:
                            counter -= 1
                            check_full_bools = np.array((busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] == busRun['ETA'].iloc[window[0]]):
                                return busRun['ETA'].iloc[window[0]]
                            elif not check_full_bools:
                                return busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx] 
     
                elif not next_full_bool:
                        return busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]
        
    elif not full_bool:
        if pickupdropoffiloc == -1:
            return busRun['ETA'][window[-1]]
        elif pickupdropoffiloc == 1:
            return busRun['ETA'][window[0]]

    

    restrictive_window, = np.where((busRun['ETA'] > URID.PickupEnd ) & (busRun['ETA'] < URID.DropoffStart))
    PickupWindow, = np.where((busRun['ETA'] >= URID.PickupStart) & (busRun['ETA'] <= URID.PickupEnd))
    DropoffWindow, = np.where((busRun['ETA'] >= URID.DropoffStart) & (busRun['ETA'] <= URID.DropoffEnd))

    max_wcCapacity = np.max(busRun['wcCapacity'].iloc[restrictive_window])
    max_amCapacity = np.max(busRun['amCapacity'].iloc[restrictive_window])
    full = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.wcOn > amCapacity(str(max_wcCapacity + URID.wcOn)))
    if full:
        # URID.PickupInsert, URID.DropoffInsert
        return np.nan, np.nan 
    elif not full:
        # URID.PickUpInsert, URID.DropoffInsert
        return checkWindow(URID, busRun, PickupWindow,1,-1), checkWindow(URID, busRun, DropoffWindow,-1,0)
        
    

       
        
        
