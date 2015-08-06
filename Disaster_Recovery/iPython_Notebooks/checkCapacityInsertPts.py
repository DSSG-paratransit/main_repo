import numpy as np
import pandas as pd 


class CapacityInsertPts():
    """
    Assumes that busRun df has wcCapacity, amCapacity columns, and that URID
    has amOn/Off and wcOn/Off columns added so it can return capacity insert points. 
    
    **Currently not implemented: apparently 2 WC + PK + AM is allowed (how often does 
    this occur in 18 month data?), so we need a check for this. Perhaps make PK 
    count as 0.9xWC?**

    **Cases left to test: 
    dropoff < pick up end:
    full pick up --> null, null
    ok pick up, full DO --> null, null
    ok pick up, ok DO --> insert pts
    dropoff > pick up end:
    full middle --> null, null
    ok middle, full pick up --> null, null 
    ok middle, ok pick up, full drop off --> null, null 
    ok all --> insert pts**
    
    Args:
    busRun (dataframe): single bus run from day's data 
    
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

        **Not implemented: check on edge case between end of time window and PU end or DO
        start. We don't have information here, so we just return that the insert is infeasible**
        

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
            # first index where bus is full 
            full_indx = np.array((self.busRun['wcCapacity'].iloc[window] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window] + URID.amOn > self.amCapacitySwitch(str(max_wcCapacity + URID.wcOn))))

            # if index where bus is full is full is unique, check capacity at next index  
            if len(self.busRun['wcCapacity'].iloc[window].loc[full_indx]) == 1:
                next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn))))
                # if the bus is still full at next index, start looping until it is not full (return index), or reach end (return null)
                if next_full_bool:
                    counter = pickupdropoffiloc
                    # check for case of pick up 
                    if (pickupdropoffiloc == 1) & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) < self.busRun['ETA'].iloc[window[-1]]):
                        while int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) < self.busRun['ETA'].iloc[window[-1]]:
                            counter += 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) == self.busRun['ETA'].iloc[window[-1]]):
                                #not enough time for pick up 
                                return np.nan 
                            elif not check_full_bools:
                                return self.busRun['ETA'].iloc[window + counter].loc[full_indx]
                    elif (pickupdropoffiloc == 1) & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) >= self.busRun['ETA'].iloc[window[-1]]):
                        #not enough time for pick up 
                        return np.nan
                    # check for case of drop off, same as above, except return DropoffStart instead of null if still full
                    # at final index 
                    elif (pickupdropoffiloc == -1) & (int(self.busRun['ETA'].iloc[window+counter].loc[full_indx]) > self.busRun['ETA'].iloc[window[0]]):
                        while int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) > self.busRun['ETA'].iloc[window[0]]:
                            counter -= 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx]) == self.busRun['ETA'].iloc[window[0]]):
                                # Must be dropped off here 
                                return URID.DropoffStart 
                            elif not check_full_bools:
                                return self.busRun['ETA'].iloc[window + counter].loc[full_indx]
                    elif (pickupdropoffiloc == -1) & (int(self.busRun['ETA'].iloc[window+counter].loc[full_indx]) <= self.busRun['ETA'].iloc[window[0]]):
                        # must be dropped off here 
                        return URID.DropoffStart 
                elif not next_full_bool:
                        return self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx]

            # if there are multiple places in PickupWindow where we go over max capacity
            # choose one that is closest to PickupEnd or DropoffStart, otherwise same as above 
            elif len(self.busRun['wcCapacity'].iloc[window].loc[full_indx]) > 1:
                    next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                    print next_full_bool
                    if next_full_bool:
                        counter = pickupdropoffiloc
                        if (pickupdropoffiloc == 1) & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) < self.busRun['ETA'].iloc[window[-1]]):
                            while int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) < self.busRun['ETA'].iloc[window[-1]]:
                                counter += 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                                if check_full_bools:
                                    continue
                                elif check_full_bools & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) == self.busRun['ETA'].iloc[window[-1]]):
                                    #not enough time for pick up 
                                    return np.nan
                                elif not check_full_bools:
                                    return self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]
                        elif (pickupdropoffiloc == 1) & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) >= self.busRun['ETA'].iloc[window[-1]]):
                            return np.nan

                        if (pickupdropoffiloc == -1) & (int(self.busRun['ETA'].iloc[window+counter].loc[full_indx][pickupdropoffindx]) > self.busRun['ETA'].iloc[window[0]]):
                            while int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) > self.busRun['ETA'].iloc[window[0]]:
                                counter -= 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > self.amCapacitySwitch(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                                if check_full_bools:
                                    continue
                                elif check_full_bools & (int(self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]) == self.busRun['ETA'].iloc[window[0]]):
                                    #return self.busRun['ETA'].iloc[window[0]]
                                    return URID.DropoffStart 
                                elif not check_full_bools:
                                    return self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]
                        elif (pickupdropoffiloc == -1) & (int(self.busRun['ETA'].iloc[window+counter].loc[full_indx]) <= self.busRun['ETA'].iloc[window[0]]):
                            return URID.DropoffStart
                        
                    # if it's not full at next index, return that index if not at end of window, otherwise return null (pick up)
                    # or dropoffstart (drop off)
                    elif not next_full_bool:
                        if pickupdropoffiloc == 1:
                            if int(self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]) >= self.busRun['ETA'].iloc[window[-1]]:
                                # not enough time for pick unicp 
                                return np.nan 
                            elif int(self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]) < self.busRun['ETA'].iloc[window[-1]]:
                                return self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]
                        elif pickupdropoffiloc == -1:
                            if int(self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]) <= self.busRun['ETA'].iloc[window[0]]:
                                return URID.DropoffStart 
                            elif int(self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]) > self.busRun['ETA'].iloc[window[0]]:
                                return self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx]

        # if the bus is not full return full time window 
        elif not full_bool:
            # a drop off 
            if pickupdropoffiloc == -1:
                return URID.DropoffEnd
                #return self.busRun['ETA'][window[-1]]
            # a pickup 
            elif pickupdropoffiloc == 1:
                return URID.PickupStart
                #return self.busRun['ETA'][window[0]]



if __name__ == "__main__":

    #this is messy, should be ported somewhere else, but for now shows a way to run it 

    capacity_obj = CapacityInsertPts(this_run)
            

    restrictive_window, = np.where((this_run['ETA'] > URID.PickupEnd ) & (this_run['ETA'] < URID.DropoffStart))
    PickupWindow, = np.where((this_run['ETA'] >= URID.PickupStart) & (this_run['ETA'] <= URID.PickupEnd))
    DropoffWindow, = np.where((this_run['ETA'] >= URID.DropoffStart) & (this_run['ETA'] <= URID.DropoffEnd))

    max_wcCapacity = this_run['wcCapacity'].iloc[restrictive_window].max()
    max_amCapacity = this_run['amCapacity'].iloc[restrictive_window].max()
    full = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.wcOn > capacity_obj.amCapacitySwitch(str(max_wcCapacity + URID.wcOn)))
    # likely to be most common case
    if URID.DropoffStart <= URID.PickupEnd:
         max_wcCapacity_PU = this_run['wcCapacity'].iloc[PickupWindow].max()
         max_amCapacity_PU = this_run['amCapacity'].iloc[PickupWindow].max()
         full_PU = (max_wcCapacity_PU + URID.wcOn > 3) & (max_amCapacity_PU + URID.wcOn > capacity_obj.amCapacitySwitch(str(max_wcCapacity_PU + URID.wcOn)))
         max_wcCapacity_DO = this_run['wcCapacity'].iloc[DropoffWindow].max()
         max_amCapacity_DO = this_run['amCapacity'].iloc[DropoffWindow].max()
         full_DO = (max_wcCapacity_DO + URID.wcOn > 3) & (max_amCapacity_DO + URID.wcOn > capacity_obj.amCapacitySwitch(str(max_wcCapacity_DO + URID.wcOn)))
         # check pick up window and then all associated cases  
         if full_PU:
              print "full somehere in pick up window "
              tmpPU = int(capacity_obj.checkWindow(URID,PickupWindow,1,-1))
              if tmpPU == URID.PickupEnd:
                  print "not enough time for pick up "
                  URID.PickupInsert, URID.DropoffInsert = np.nan, np.nan
              elif (tmpPU < URID.PickupEnd) and (full_DO):
                  print "pick up okay, full somewhere in drop off window"
                  tmpDO = int(capacity_obj.checkWindow(URID, DropoffWindow,-1,0))
                  if tmpDO == URID.DropoffEnd:
                      print "not enough time for drop off"
                      URID.PickupInsert, URID.DropoffInsert = np.nan, np.nan
                  elif tmpDO < URID.DropoffEnd:
                      print "returning pick up and drop off inserts"
                      URID.PickupInsert, URID.DropoffInsert = int(capacity_obj.checkWindow(URID,PickupWindow,1,-1)), int(capacity_obj.checkWindow(URID, DropoffWindow,-1,0))
              elif (tmpPU < URID.PickupEnd) and not (full_DO):
                  print "returning pick up and drop off inserts, drop off never full"
                  URID.PickupInsert, URID.DropoffInsert = int(capacity_obj.checkWindow(URID,PickupWindow,1,-1)), URID.DropoffEnd
         elif not (full_PU) and (full_DO):
             print "pick up never full, drop off full somewhere"
             tmpDO = int(capacity_obj.checkWindow(URID, DropoffWindow,-1,0))
             if tmpDO == URID.DropoffEnd:
                 print "not enough time for drop off"
                 URID.PickupInsert, URID.DropoffInsert = np.nan, np.nan
             elif tmpDO < URID.DropoffEnd:
                 print "returning pick up and drop off inserts, pick up never full "
                 URID.PickupInsert, URID.DropoffInsert = URID.PickupStart, int(capacity_obj.checkWindow(URID, DropoffWindow,-1,0))
         elif not full_PU and not full_DO:
                 print "entire window available!"
                 URID.PickupInsert, URID.DropoffInsert = URID.PickupStart, URID.DropoffEnd
             
    if URID.DropoffStart > URID.PickupEnd:
        if full:
            # URID.PickupInsert, URID.DropoffInsert
            URID.PickupInsert, URID.DropoffInsert =  np.nan, np.nan 
        elif not full:
            if np.isnan(int(capacity_obj.checkWindow(URID.PickupWindow,1,-1))):
                URID.PickupInsert, URID.DropoffInsert = np.nan, np.nan
            else:
                URID.PickupInsert, URID.DropoffInsert = int(capacity_obj.checkWindow(URID, PickupWindow,1,-1)), int(capacity_obj.checkWindow(URID, DropoffWindow,-1,0))

else:
    print "Importing checkCapacityInsertPts"
    #call in the following way:
    #from checkCapacityInsertPts import CapacityInsertPts
    #then use above syntax given a single busRun and URID
    
