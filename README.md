# dssg_paratransit

#Access_Analysis_Rproject folder:

The Rproj has a directory called "Scripts" that contains various scripts in Python and R, which help do different analyses of the data.

Place all relevant data .csv files in the "data" directory to have easy access to it.


#System Recovery Folder:

-Should contain all files related to our system recovery algorithm
-The main file should be calling functions from the other files to run our algorithm

#What our algorithm does:
- Takes real time data 
- Cleans data
- Accepts and formats unscheduled requests
- Finds the best insertion for unscheduled requests onto a previously scheduled bus route
-Compares the cost for handling unscheduled requests by inserting onto scheduled bus routes, calling a taxi, or creating a new bus run

#To install and run webapp:
##OSX install instructions (Maverick & Yosemite):
1. Installing python with Anaconda<br>
   	
Download an install Python 2.7 from [`here`] (http://continuum.io/downloads#all) (keep the default settings).


2. Obtaining the files<br>
    Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 

3.  Obtaining the demo file<br>
	
	(cannot be stored on GitHub) <br>

	Copy file *qc\_streaming\_DEMO.csv* from *Google Drive/DSSG Program/Project Folders/Paratransit Group/Data* to *System\_recovery/webapp/data folder*. 

4. Starting a Python virtual environment
 <br>
 (skip steps 4,9 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)

   ~~~bash
   cd Python_venv
   conda create -n venv python=2.7
   source activate venv
   cd..
   ~~~

   Now you are in the virtual environment! 


5. Installing the required packages
    ~~~bash
	pip install -r Python_venv/requirements.txt
	~~~

6. Run the webapp
    ~~~bash
	cd System_Recovery/webapp
	python run.py
	~~~
    
7. Navigate to [`localhost:5000/admin`](localhost:5000/admin)

7. Running the demo
 <br>

	Input qc\_streaming_DEMO.csv as the demo name.
	You can test with bus number 6080 and time 13:30.

8. Exit virtual environment
    ~~~bash
	source deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it (skip step 5).
	
    
##Windows 7 install instructions:
1. Installing Python with Anaconda
 <br>
   	
 Download an install Python 2.7 from [`here`] (http://continuum.io/downloads#all) (keep the default settings).

3. Obtaining the files<br>
     Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 


3. Obtaining the demo file<br>
	
	(cannot be stored on GitHub) <br>

	Copy file *qc\_streaming\_DEMO.csv* from *Google Drive\DSSG Program\Project Folders\Paratransit Group\Data* to *System\_recovery\webapp\data folder*. 
	
	
3. Setting up a Python virtual environment
   <br>
    (skip steps 3,8 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)

   <br>
	~~~bash
	cd Python_venv
	conda create -n venv python
	activate venv
	cd ..
	~~~

    Now you are in the virtual environment!

5. Installing the required packages
   <br>
    ~~~bash
	pip install -r Python_venv\requirements_Windows.txt
	~~~
6. Run the webapp
   <br>

    ~~~bash
	cd System_Recovery\webapp
	python run.py
    ~~~~

7. Navigate to [`localhost:5000/admin`](localhost:5000/admin)

7. Running the demo
<br>
	Input qc\_streaming_DEMO.csv as the demo name.
	You can test with bus number 6080 and time 13:30.
    
8. Exit the virtual environment
 <br>

	~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it (skip step 5).        




