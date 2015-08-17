Instructions to run the webapp on:



###Windows 7
-------------
1. Installing Python

	Go to 
	[`https://www.python.org/downloads/release/python-2710/`](https://www.python.org/downloads/release/python-2710/) and download the Windows installer. Install Python 2.7.10. If the default path is *C:\Python27*, add *C:\Python27* and *C:\Python27\Scripts* to your path environment variables: go to System Properties->Advanced->Environment Variables and attach to the System Path variable *;C:\Python27;C:\Python27\Scripts*)

2. Installing Visual C++ Compiler

	(it is needed to run the Python numerical packages)
	
	Install version 9.0.0 from [`here`] (http://www.microsoft.com/en-us/download/details.aspx?id=44266).
	

1. Obtaining the files

	Go to 
	
	[`https://github.com/DSSG-paratransit/main_repo/tree/newbranch/`](https://github.com/DSSG-paratransit/main_repo/tree/webapp/)
	
	and click on Download ZIP on the lower right. Unzip the materials in a folder of your choice. Navigate to the *main_repo-newbranch* directory.
	
2.  Obtaining the demo file
	
	(cannot be stored on GitHub)

	Copy file *qc\_streaming.csv* from *Google Drive/DSSG Program/Project Folders/Paratransit Group/Data* to *Disaster\_recovery/webapp/data folder*.  
	



2. Setting up a virtual environment 

	(skip steps 5,6,10 if you want to install the packages directly on your computer; using a virtual environment aims to avoid some dependency conflicts)

	~~~
	pip install virtualenv
	~~~


3. Starting the Python virtual environment

	~~~bash
	cd Python_venv
	virtualenv venv
	venv\Scripts\activate
	cd ..
	~~~

	Now you are in the virtual environment!

4. Installing the required packages. The file 	*requirements_Windows.txt* contains a list of them.

	~~~bash
	pip install -r requirements_Windows.txt
	~~~

5. Run the webapp

	~~~bash
	cd Disaster_Recovery\webapp
	python run.py
	~~~
	
6. Navigate to [`localhost:5000/admin`](localhost:5000/admin).

6. Exit the virtual environment

	~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it.
	

	








