![DSSG-heading](/_images/DataScienceForSocialGood.png)
# King County Metro Paratransit #
# Rerouting Solutions and Ride Analysis #

DREU Fellow: Emily Andrulis  
DSSG Fellows: Rohan Aras, Frank Fineis, Kristen Garofali, Kivan Polimis  
eScience Data Scientists: Joseph Hellerstein, Valentina Staneva  
Project Lead: Dr. Anat Caspi, Director, Taskar Center for Accessible Technology

Follow our [project's blog](http://dssg-paratransit.github.io/blog/)

# Access_Analysis_Project folder:

The `scripts` directory contains various scripts in Python and R for different analyses of the data such as calculate rider cost per boarding and trip deadhead time. The `notebooks` folder contains Python notebooks of analyses that incorporate functions found in `scripts`. The `reports` directory contains the .Rmd code to create reports and .html output.

Place all relevant data .csv files in the `data` directory to have easy access to it.

# System_Recovery folder:
- Contains all files related to our system recovery algorithm
- `run.py` calls the core algorithm functions and starts a web application to reroute buses or individuals

# What our algorithm does:
- Takes real time data 
- Cleans data
- Accepts and formats unscheduled requests
- Finds the best insertion for unscheduled requests onto a previously scheduled bus route
- Compares the cost for handling unscheduled requests by inserting onto scheduled bus routes, calling a taxi, or creating a new bus run

# To install and run webapp:
## OSX install instructions (Maverick & Yosemite):
1. Installing python with Anaconda<br>
   	
  Download an install Python 2.7 from [here](http://continuum.io/downloads#all) (keep the default settings).

2. Obtaining the files<br>
    Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 

3.  Obtaining the demo file<br>
	
	(cannot be stored on GitHub) <br>

	Copy file `qc_streaming_DEMO.csv` from *Google Drive/DSSG Program/Project Folders/Paratransit Group/Data* to *System\_Recovery/webapp/data folder*. 

4. Starting a Python virtual environment
 <br>
 (skip steps 4 and 9 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)

   ~~~bash
   conda create -n venv python=2.7
   source activate venv
   ~~~

   Now you are in the virtual environment! 


5. Installing the required packages
  ~~~bash
	cd Python_venv
	pip install -r requirements.txt
	cd ..
  ~~~

6. Run the webapp
  ~~~bash
	cd System_Recovery/webapp
	python run.py
	~~~
    
7. Launching the webapp automatically opens [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

8. Running the demo
 <br>

	Input `qc_streaming_DEMO.csv` as the demo name.
	You can test with bus number 6080 and time 13:30.

9. Exit virtual environment
  ~~~bash
	source deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it (skip step 5).
	
    
## Windows 7 install instructions:
1. Installing Python with Anaconda

  Download an install Python 2.7 from [here](http://continuum.io/downloads#all) (keep the default settings).

2. Obtaining the files<br>
     Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 

3. Obtaining the demo file<br>
	
	(cannot be stored on GitHub) <br>

	Copy file `qc_streaming_DEMO.csv` from *Google Drive\DSSG Program\Project Folders\Paratransit Group\Data* to *System\_Recovery\webapp\data folder*. 
	
	
4. Starting a Python virtual environment
 <br>
 (skip steps 4 and 9 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)

   ~~~bash
   conda create -n venv python=2.7
   source activate venv
   ~~~

   Now you are in the virtual environment! 


5. Installing the required packages
  ~~~bash
	cd Python_venv
	pip install -r requirements_Windows.txt
	cd ..
  ~~~

6. Run the webapp
   <br>

  ~~~bash
	cd System_Recovery\webapp
	python run.py
    ~~~~

7. Launching the webapp automatically opens [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

8. Running the demo
<br>
	Input `qc_streaming_DEMO.csv` as the demo name.
	You can test with bus number 6080 and time 13:30.
    
9. Exit the virtual environment
 <br>

	~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it (skip step 5).        




