class CapacityInsertPts():
    """

    """

    def __init__(self, busRun):
        """

        """

        self.busRun = busRun

    def amCapacity(self,window):
        """

        """

        wcCapacityTotal = str(np.max(self.busRun['wcCapacity'].iloc[window]) + URID.wcOn)
        return {
            '0': 12,
            '1': 8,
            '2': 4,
            '3': 0}.get(wcCapacityTotal,-1000)

    def checkWindow(self, window, dropoffpickupiloc, dropoffpickupindx):
        """


        """
        max_wcCapacity = np.max(self.busRun['wcCapacity'].iloc[window])
        max_amCapacity = np.max(self.busRun['amCapacity'].iloc[window])
        full_bool = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.amOn > amCapacity(str(max_wcCapacity + URID.wcOn)))

        if full_bool:
            full_indx = np.array((self.busRun['wcCapacity'].iloc[window] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window] + URID.amOn > amCapacity(str(max_wcCapacity + URID.wcOn))))

            # check capacity in window if max capacity is unique   
            if len(self.busRun['wcCapacity'].iloc[window].loc[full_indx]) == 1:
                next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx] + URID.wcOn))))
                if next_full_bool:
                    counter = pickupdropoffiloc
                    if pickupdropoffiloc == 1:
                        while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] < self.busRun['ETA'].iloc[window[-1]]:
                            counter += 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
                            if check_full_bools:
                                continue
                            elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] == self.busRun['ETA'].iloc[window[-1]]):
                                return self.busRun['ETA'].iloc[window[-1]]
                            elif not check_full_bools:
                                return self.busRun['ETA'].iloc[window + counter].loc[full_indx]
                    elif pickupdropoffiloc == -1:
                        while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx] > self.busRun['ETA'].iloc[window[0]]:
                            counter -= 1
                            check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx] + URID.wcOn))))
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
                    next_full_bool = np.array((self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                    if next_full_bool:
                        counter = pickupdropoffiloc
                        if pickupdropoffiloc == 1:
                            while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] < self.busRun['ETA'].iloc[window[-1]]:
                                counter += 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
                                if check_full_bools:
                                    continue
                                elif check_full_bools & (self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] == self.busRun['ETA'].iloc[window[-1]]):
                                    return self.busRun['ETA'].iloc[window[-1]]
                                elif not check_full_bools:
                                    return self.busRun['ETA'].iloc[window + counter].loc[full_indx][pickupdropoffindx]
                        if pickupdropoffiloc == -1:
                            while self.busRun['ETA'].iloc[window + pickupdropoffiloc].loc[full_indx][pickupdropoffindx] > self.busRun['ETA'].iloc[window[0]]:
                                counter -= 1
                                check_full_bools = np.array((self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn > 3) & (self.busRun['amCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.amOn > amCapacity(str(self.busRun['wcCapacity'].iloc[window + counter].loc[full_indx][pickupdropoffindx] + URID.wcOn))))
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

    max_wcCapacity = np.max(busRun['wcCapacity'].iloc[restrictive_window])
    max_amCapacity = np.max(busRun['amCapacity'].iloc[restrictive_window])
    full = (max_wcCapacity + URID.wcOn > 3) & (max_amCapacity + URID.wcOn > capacity_obj.amCapacity(str(max_wcCapacity + URID.wcOn)))
    if full:
        # URID.PickupInsert, URID.DropoffInsert
        return np.nan, np.nan 
    elif not full:
        # URID.PickUpInsert, URID.DropoffInsert
        return capacity_obj.checkWindow(PickupWindow,1,-1), capacity_obj.checkWindow(DropoffWindow,-1,0)

else:
    print "Importing checkCapacityInsertPts"
    #call in the following way:
    #from checkCapacityInsertPts import CapacityInsertPts
    #then use above syntax given a single busRun and URID
    
