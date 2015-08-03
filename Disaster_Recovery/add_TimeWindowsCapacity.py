import pandas as pd
import numpy as np 

class PassengerCounter():

    """ 
    Class to implement the calculation for both ambulatory and wheelchair 
    capacity from start time to a given "checkpoint," i.e. end of run.
    **Currently not implemented: a check that for a given passenger the "On"
    column equals the "Off" column** 

    Attributes:
    on (array): column from df that has entries for WC/AM numbers at each time step 
    off (array): column from df that has entries for WC/AM numbers at each time step 
    
    """
    
    def __init__(self, on,off):

        """
        
        Args: 
        on (array): column from df that has entries for WC/AM numbers at each time step 
        off (array): column from df that has entries for WC/AM numbers at each time step 
        
        """
        self.on = on
        self.off = off


    def passenger_sum(self, thesum, iter):

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

  

    def passenger_count_at_checkpoint(self, checkpoint):

        """
        
        Args:
        checkpoint (int): index of each timestep at which passenger(s) get on/off bus 

        Returns:
        Difference between passengers getting on and off bus at given checkpoint (timestep) 

        """
        on_count = reduce(self.passenger_sum, self.on[:checkpoint],0)
        off_count = reduce(self.passenger_sum, self.off[:checkpoint],0)

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











class TimeWindowsCapacity():

    """
    Class to calculate and add the time windows and add capacity columns from pre-exisitng dataframe.

    Attributes:
    data (dataframe): the dataframe containing the single day's ride information
    


    """

    def __init__(self,data):
        self.data = data 

    def add_TimeWindows(self, windows):
        """
        Function to both calculate and add the time windows 
        to the existing dataframe. Time windows come from 
        SchTime and ETA. 
        
        Args: 
        windows (int): size of pickup/dropoff windows in seconds 

        Returns: 
        dataframe with PickupStart, PickupEnd, DropoffStart, and DropoffEnd columns appended 
        
        """


        etas = self.data.ix[:,"ETA"]
        schtime =self.data.ix[:,"SchTime"]
        Activity = self.data.ix[:, "Activity"]
        ReqLate = self.data.ix[:, "ReqLate"]

        schtime_arr = np.array(schtime.tolist())
        nrow = self.data.shape[0]
        PickupStart = np.zeros(nrow); PickupEnd = np.zeros(nrow)
        DropoffStart = np.zeros(nrow); DropoffEnd = np.zeros(nrow)

        for x in range(0, nrow):

            #make dropoff window when there's no required drop off time
            if (Activity[x] == 1) & (ReqLate[x] <0):
                DropoffStart[x] = etas[x]-3600
                DropoffEnd[x] = etas[x]+3600

            #make dropoff window when there IS a required drop off time: 1hr before ReqLate time
            if (Activity[x] == 1) & (ReqLate[x] >0):
                DropoffStart[x] = etas[x]-3600
                DropoffEnd[x] = ReqLate[x]  

            #schtime is in the middle of the pick up window
            if Activity[x] == 0:
                PickupStart[x] = schtime[x]-(windows/2)
                PickupEnd[x] = schtime[x]+(windows/2)

        self.data.insert(len(self.data.columns), 'PickupStart',  pd.Series((PickupStart), index=self.data.index))
        self.data.insert(len(self.data.columns), 'PickupEnd',  pd.Series((PickupEnd), index=self.data.index))
        self.data.insert(len(self.data.columns), 'DropoffStart',  pd.Series(DropoffStart, index=self.data.index))
        self.data.insert(len(self.data.columns), 'DropoffEnd',  pd.Series(DropoffEnd, index=self.data.index))

        return self.data



    def create_OnOffcols(self, wc=True):

        """
    
        Args:
        wc (bool): default True

        Returns:
        two arrays that are on and off columns, respectively 

        """

        no_shows = np.where(self.data['SchedStatus'] != 1.)
        self.data['SpaceOn'].iloc[no_shows] = np.NAN
        self.data['SpaceOff'].iloc[no_shows] = np.NAN

        if wc:
            allcols_On = [self.data['SpaceOn'].str.split(",",expand=True)[i].str.extract('(?P<letter>WG|WH|PK|WX|SC|OR)(?P<digit>\d)') for i in range(self.data['SpaceOn'].str.split(",",expand=True).shape[1])]
            allcols_Off = [self.data['SpaceOff'].str.split(",",expand=True)[i].str.extract('(?P<letter>WG|WH|PK|WX|SC|OR)(?P<digit>\d)') for i in range(self.data['SpaceOff'].str.split(",",expand=True).shape[1])]
        else:
            allcols_On = [self.data['SpaceOn'].str.split(",",expand=True)[i].str.extract('(?P<letter>AM)(?P<digit>\d)') for i in range(self.data['SpaceOn'].str.split(",",expand=True).shape[1])]
            allcols_Off = [self.data['SpaceOff'].str.split(",",expand=True)[i].str.extract('(?P<letter>AM)(?P<digit>\d)') for i in range(self.data['SpaceOff'].str.split(",",expand=True).shape[1])]


        for i in range(len(allcols_On)):
            allcols_On[i].digit[pd.isnull(allcols_On[i].digit)] = 0
            allcols_On[i].digit[~pd.isnull(allcols_On[i].digit)] = [int(j) for j in allcols_On[i].digit[~pd.isnull(allcols_On[i].digit)]] 
            allcols_Off[i].digit[pd.isnull(allcols_Off[i].digit)] = 0
            allcols_Off[i].digit[~pd.isnull(allcols_Off[i].digit)] = [int(j) for j in allcols_Off[i].digit[~pd.isnull(allcols_Off[i].digit)]]


        return sum([allcols_On[i].digit for i in range(len(allcols_On))]), sum([allcols_Off[i].digit for i in range(len(allcols_Off))])

    def add_Capacity(self, busDateCol=False, wc=True):

        """

        Args:
        busDateCol (bool): default False, make True if the dataframe includes different service dates as well as bus runs
        wc (bool): default True, make False if doing am capacity 

        Returns:
        original dataframe with WC and AM columns added 

        """

        no_shows = np.where(self.data['SchedStatus'] != 1.)
        self.data['SpaceOn'].iloc[no_shows] = np.NAN
        self.data['SpaceOff'].iloc[no_shows] = np.NAN

        self.data['wcOn'], self.data['wcOff'] = self.create_OnOffcols()
        self.data['amOn'], self.data['amOff'] = self.create_OnOffcols(wc=False)
        self.data['wcCapacity'] = ""
        self.data['amCapacity'] = ""


        if busDateCol:
            zipped = np.unique(zip(self.data['ServiceDate'],self.data['Run']))
            for i in range(len(zipped)):
                this_run = self.data[(self.data['Run'] == zipped[i][1]) & (self.data['ServiceDate'] == zipped[i][0])]
                on_wc = np.array(this_run['wcOn'])
                off_wc = np.array(this_run['wcOff'])
                p_wc = PassengerCounter(on_wc,off_wc)
                on_am = np.array(this_run['amOn'])
                off_am = np.array(this_run['amOff'])
                p_am = PassengerCounter(on_am, off_am)
                self.data['wcCapacity'].loc[str(run)] = [p_wc.passenger_count_at_checkpoint(i) for i in range(1,len(on_wc)+1)]
                self.data['amCapacity'].loc[str(run)] = [p_am.passenger_count_at_checkpoint(i) for i in range(1,len(on_am)+1)]

        if not busDateCol:
            for run in np.unique(self.data['Run']):
                this_run = self.data[(self.data['Run'] == run)]
                on_wc = np.array(this_run['wcOn'])
                off_wc = np.array(this_run['wcOff'])
                p_wc = PassengerCounter(on_wc,off_wc)
                on_am = np.array(this_run['amOn'])
                off_am = np.array(this_run['amOff'])
                p_am = PassengerCounter(on_am, off_am)
                runbool = run == self.data['Run']
                self.data['wcCapacity'].loc[runbool] = [p_wc.passenger_count_at_checkpoint(i) for i in range(1,len(on_wc)+1)]
                self.data['amCapacity'].loc[runbool] = [p_am.passenger_count_at_checkpoint(i) for i in range(1,len(on_am)+1)]

        return self.data

    def addtoRun_TimeCapacity(self, windows):

        """
        Args:
        windows (int): pickup/dropoff time window in seconds

        Returns: 
        dataframe updated with time windows and capacity columns added 

        """
        
        data_updated = self.add_TimeWindows(windows)
        data_updated = self.add_Capacity() 
        return data_updated 




        





if __name__ == "__main__":
    df = pd.DataFrame.from_csv('single_clean_day.csv', header=0, sep=',')
    df_obj = TimeWindowsCapacity(df)
    df_updated = df_obj.addtoRun_TimeCapacity(1800.)
    df_updated.to_csv('tmp_wtimecapacity.csv', sep=',')
    
else:
    print "Importing add_TimeWindowsCapacity"
    # call in the following way: 
    # df = pd.DataFrame.from_csv(sys.argv[1], header=0, sep=',')
    # df_obj = TimeWindowsCapacity(df)
    # df_updated = df_obj.addtoRun_TimeCapacity(sys.argv[2])
    # return df_updated 

             

