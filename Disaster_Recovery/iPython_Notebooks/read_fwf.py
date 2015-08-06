import pandas as pd
import numpy as np
import sys



"""
	This script processes data from the 15 minutes csv files. They are fixed-width-delimited files (as opposed to standard comma-delimited files, and if they are read in the usual way some of the columns in the end containing several strings (like the PassOn and PassOff columns) get messed up). So instead they need to be read using the read_fwf function in pandas.

Input: 	arg1 - the name of the input file
        	arg2 - the name of the output file (optional)


Output: 
	If a second argument is passed the processed dataset is saved as a tab-delimited .csv file
	

Usage: 	from command line 
	>> python read_fwf.py fixed_width_file.csv tab_delimited_file.csv

       	from within ipython
       	>> % run python read_fwf.py fixed_width_file.csv
	(here I do not write the output to a file but I directly create a pandas dataframe called data)

Note: The types are hard-coded: you can modify usage based on your needs 
        ('ETA','DwellTime','Activity' are floats as they contain NaNs
        and cannot be automatically converted to integers)


Warning: this relies on the structure of files not changing

      
"""


def main():

    filename = sys.argv[1]
    print('Processing file '+ filename)

    # read the data
    data = read(filename)

    #write the data
    if len(sys.argv)>2:
        data.to_csv(sys.argv[2],sep = '\t')

def read(filename):
    """ 
      
        reads a fwf file into a pandas data frame
        
        Usage: data = read(filename)
        
        Note: ('ETA','DwellTime','Activity' are floats as they contain NaNs
                and cannot be automatically converted to integers)
    """    
    
    # creating the widths of each column
    widths = [12,21,12,12,12,9,12,12,21,255,255,25,25,12,12,12,12,17,51,51,12]
    
    # creating colspecs (containing starting and ending point [) of a column)
    cumsum = [sum(widths[:i+1]) for i in range(len(widths))]
    
    # excluding the commas
    cumsum0 = [0]+cumsum[:-1]
    cumsum_short = [item-1 for item in cumsum]
    colspecs = list(zip(cumsum0,cumsum_short))
    
    # reading the file
    try:
        data = pd.read_fwf(filename,colspecs = colspecs,skiprows = [1], dtype = {'ProviderId': 'str', 'ETA': 'str'})
    except(IOError):
        print('This file does not exist. Please, check the filename or the directory.')
        sys.exit()
    
    # spectifying explicitly the data types
    data = data.astype('object')
    numeric_list = ['LON','LAT','DwellTime']
    data[numeric_list] = data[numeric_list].astype('float')
    return(data)


if __name__ == '__main__':
    main()

