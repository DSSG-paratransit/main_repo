# dssg_paratransit

Use the Access_Analysis_Rproject folder to get the Rproject.

The Rproj has a directory called "R" that contains various scripts for QC'ing and accessing more information contained in the trip data thus far.

Place all relevant data .csv files in the "data" directory to have easy access to it.


#PYTHON SCRIPTS FOLDER:
- given single_day_clean.csv, run add_Time_Windows.py to add relevant pickup and time windows to the file.
- get_URIDs.py will make, from the pandas.data.frame make in add_Time_Windows.py, a list of URID-class objects for all unhandled request id's
- get_busRuns.py will take the data from add_Time_Windows.py and a given bus run number and spit out the remaining relevant route information for the rest of the day AFTER the breakdown time
- get_buses_realtime.ipynb: IPython Notebook that runs through how to use these scripts

