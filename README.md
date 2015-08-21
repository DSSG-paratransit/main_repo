# dssg_paratransit

#Access_Analysis_Rproject folder:

The Rproj has a directory called "Scripts" that contains various scripts in Python and R, which help do different analyses of the data.

Place all relevant data .csv files in the "data" directory to have easy access to it.


#System Recovery Folder:

-Should contain all files related to our disaster recovery algorithm
-The main file should be calling functions from the other files to run our algorithm

#What our algorithm does:
- Takes real time data 
- Cleans data
- Accepts and formats unscheduled requests
- Finds the best insertion for unscheduled requests onto a previously scheduled bus route
-Compares the cost for handling unscheduled requests by inserting onto scheduled bus routes, calling a taxi, or creating a new bus run

#To install and run webapp:
##OSX install instructions:
1. Installing python <br>
    Go to ['https://www.python.org/downloads/release/python-2710/'](https://www.python.org/downloads/release/python-2710/) and download the Mac installer. Install Python 2.7.10.

    <br>
    Install [Anaconda]('http://continuum.io/downloads') by downloading the command-line installer.

2. Obtaining the files
    Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 

3. Setting up a virtual environment
    (skip steps 3,4,8 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)
    ~~~
	pip install virtualenv
	~~~
    If pip is not installed on your computer (it is included with python versions 2.7.9 and above), you can install it in one of the following ways:
    ~~~bash
	sudo easy_install pip
	~~~

	or 

	~~~bash
	sudo brew install pip
	~~~

	If you have neither easy_install nor brew then go 	through these tutorials to install one of them.

	[easy_install] (https://pythonhosted.org/setuptools/easy_install.html#installing-easy-install)
	[brew](http://brew.sh/)

4. Starting Anaconda virtual environment
   ~~~bash
	conda create -n venv python=2.7
	~~~

	~~~bash
	conda activate venv
	~~~

	Now you are in the virtual environment! Next, you need to add Python to your path environment variables:

	~~~bash
	which python
	~~~
	
	Take whatever output you get from this call, for example,
	~~~bash
	~/anaconda/envs/venv/bin/python
	~~~

	~~~bash
	export PATH=~/anaconda/envs/venv/bin/python:$PATH
	~~~


5. Installing the required packages
    ~~~bash
	pip install -r Python_venv/requirements.txt
	~~~

6. Run the webapp
    ~~~bash
	cd Disaster_Recovery/webapp
	python run.py
	~~~
    
7. Navigate to [`localhost:5000/admin`](localhost:5000/admin)
    Enter AWS access key and secret key, or demo file.

8. Exit virtual environment
    ~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it.
	
    
##Windows install instructions:
1. Installing Python
    Go to     [`https://www.python.org/downloads/release/python-2710/`](https://www.python.org/downloads/release/python-2710/) and download the Windows installer. Install Python 2.7.10. If the default path is *C:\Python27*, add *C:\Python27* and *C:\Python27\Scripts* to your path environment variables: go to System Properties->Advanced->Environment Variables and attach to the System Path variable *;C:\Python27;C:\Python27\Scripts*)

2. Installing Visual C++ Compiler
    (it is needed to run the Python numerical packages)
	
	Install version 9.0.0 from [`here`] (http://www.microsoft.com/en-us/download/details.aspx?id=44266).

3. Obtaining the files
     Go to ['https://github.com/DSSG-paratransit/main_repo/tree/master'](https://github.com/DSSG-paratransit/main_repo/tree/master) and click on Download Zip in the lower right. Unzip the materials into the folder of your choice. 


3. Setting up a virtual environment
    (skip steps 3,4,8 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)
    ~~~
	pip install virtualenv
	~~~

4. Starting the Python virtual environment

	~~~bash
	cd Python_venv
	virtualenv venv
	venv\Scripts\activate
	cd ..
	~~~

    Now you are in the virtual environment!

5. Installing the required packages
    ~~~bash
	pip install -r Python_venv/requirements_Windows.txt
	~~~
6. Run the webapp

    ~~~bash
	cd Disaster_Recovery\webapp
	python run.py
    ~~~~

7. Navigate to [`localhost:5000/admin`](localhost:5000/admin)
    
8. Exit the virtual environment

	~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it.        




