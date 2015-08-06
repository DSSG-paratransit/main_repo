import numpy as np
import pandas as pd 


class CapacityInsertPts():
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


    def __init__(self, busRun):
        """
        Args:
        busRun (dataframe): single bus run from day's data 

        """

        self.busRun = busRun

    def amCapacitySwitch(self, wcCapacityTotal):
        """
        Quick function to do something 
        like switch statements in python.
        
        Args: 
        wcCapacityTotal (string): str(max_wcCapacity + URID.wcOn), basically total wc capacity 
        given max wc capacity in that time window and URID wc capacity in string form 
        
        Returns:
        appropriate am capacity given this total wc capacity, else -1000 if wc capacity entered is not in 
        dictionary. need to catch cases where wc capacity is over 3 but am capacity is otherwise acceptably low 

        **Currently not implemented: cases where package is added and more am passengers are thus allowed**
        

        """

        #wcCapacityTotal = str(self.busRun['wcCapacity'].iloc[window].max() + URID.wcOn)
        return {
            '0': 14,
            '1': 10,
            '2': 6,
            '3': 2}.get(wcCapacityTotal,-1000)

    def checkWindow(self, URID, window, pickupdropoffiloc, pickupdropoffindx):
        """
        
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
        URID (class instance): contains all info for unscheduled request 
        window (array): window in which to check capacity, i.e. PickupWindow/DropoffWindow
        pickupdropoffiloc (int): used for indexing window array. For pickups we want closest to PickupEnd, i.e. + 1. For dropoffs we want closest to DropoffStart, i.e. -1.
        pickupdropoffindx (int): used for indexing bool array in the event of non-unique max capacity. For pickups
        we want closest to PickupEnd, i.e. -1. For dropoffs we want closest to DropoffStart, i.e. 0.
        
        Returns:
        URID.PickupInsert or URID.DropoffInsert depending on how it's called 


        """
        max_wcCapacity = self.busRun['wcCapacity'].iloc[window].max()
        max_amCapacity = self.busRun['amCapacity'].iloc[window].max()
        full_bool = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.amOn > self.amCapacitySwitch(str(max_wcCapacity + URID.wcOn)))

        if full_bool:
            full_indx = np.array((self.busRun['wcCapacity'].iloc[window] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window] + URID.amOn > self.amCapacitySwitch(str(max_wcCapacity + URID.wcOn))))

            # check capacity in window if max capacity is unique   
            if len(self.busRun['wcCapacity'].iloc[window].loc[full_indx]) == 1:
                next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn))))
                if next_full_bool:
                    counter = pickupdropoffiloc
                    if pickupdropoffiloc == 1:
                        while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] < self.busRun['ETA'].iloc[window[-1]]:
                            counter += 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] == self.busRun['ETA'].iloc[window[-1]]):
                                return self.busRun['ETA'].iloc[window[-1]]
                            elif not check_full_bools:
                                return self.busRun['ETA'].iloc[window + counter].loc[full_indx]
                    elif pickupdropoffiloc == -1:
                        while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] > self.busRun['ETA'].iloc[window[0]]:
                            counter -= 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] == self.busRun['ETA'].iloc[window[0]]):
                                return self.busRun['ETA'].iloc[window[0]]
                            elif not check_full_bools:
                                return self.busRun['ETA'].iloc[window + counter].loc[full_indx]
                elif not next_full_bool:
                        return self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx]

            # if there are multiple places in PickupWindow where we go over max capacity
            # choose one that is closest to PickupEnd
            elif len(self.busRun['wcCapacity'].iloc[window].loc[full_indx]) > 1:
                    next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                    if next_full_bool:
                        counter = pickupdropoffiloc
                        if pickupdropoffiloc == 1:
                            while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] < self.busRun['ETA'].iloc[window[-1]]:
                                counter += 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                                if check_full_bools:
                                    continue
                                elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] == self.busRun['ETA'].iloc[window[-1]]):
                                    return self.busRun['ETA'].iloc[window[-1]]
                                elif not check_full_bools:
                                    return self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]
                        if pickupdropoffiloc == -1:
                            while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] > self.busRun['ETA'].iloc[window[0]]:
                                counter -= 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                                if check_full_bools:
                                    continue
                                elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] == self.busRun['ETA'].iloc[window[0]]):
                                    return self.busRun['ETA'].iloc[window[0]]
                                elif not check_full_bools:
                                    return self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx] 

                    elif not next_full_bool:
                            return self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]

        elif not full_bool:
            if pickupdropoffiloc == -1:
                return self.busRun['ETA'][window[-1]]
            elif pickupdropoffiloc == 1:
                return self.busRun['ETA'][window[0]]


if __name__ == "__main__":

    capacity_obj = CapacityInsertPts(busRun)
            

    restrictive_window, = np.where((busRun['ETA'] > URID.PickupEnd ) & (busRun['ETA'] < URID.DropoffStart))
    PickupWindow, = np.where((busRun['ETA'] >= URID.PickupStart) & (busRun['ETA'] <= URID.PickupEnd))
    DropoffWindow, = np.where((busRun['ETA'] >= URID.DropoffStart) & (busRun['ETA'] <= URID.DropoffEnd))

    max_wcCapacity = busRun['wcCapacity'].iloc[restrictive_window].max()
    max_amCapacity = busRun['amCapacity'].iloc[restrictive_window].max()
    full = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.wcOn > capacity_obj.amCapacitySwitch(str(max_wcCapacity + URID.wcOn)))
    if full:
        # URID.PickupInsert, URID.DropoffInsert
        URID.PickupInsert, URID.DropoffInsert =  np.nan, np.nan 
    elif not full:
        # URID.PickUpInsert, URID.DropoffInsert
        URID.PickupInsert, URID.DropoffInsert = capacity_obj.checkWindow(URID, PickupWindow,1,-1), capacity_obj.checkWindow(URID, DropoffWindow,-1,0)

else:
    print "Importing checkCapacityInsertPts"
    #call in the following way:
    #from checkCapacityInsertPts import CapacityInsertPts
    #then use above syntax given a single busRun and URID
    
