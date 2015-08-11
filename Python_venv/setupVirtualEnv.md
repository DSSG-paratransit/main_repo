Instructions to setup a virtual environment and run a rescheduling example within an ipython notebook. This environment does not include any dependencies to run the web app.


###OS X
-------------

1. Obtaining the files

	Download the following repository:
	
	[`https://github.com/valentina-s/main_repo`](https://github.com/valentina-s/main_repo)
	
	
	Copy file single\_day\_clean.csv from Google Drive/DSSG Program/Project Folders/Paratransit Group/Data to Access_Analysis_Rproject/data folder.  
	
	~~~
	cd main_repo
	~~~



2. Installing virtualenv

	~~~
	pip install virtualenv
	~~~

	If pip is not installed on your computer (it is 	included with python versions 2.7.9 and above), 	you can install it in one of the following ways:

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

3. Starting the Python virtual environment

	~~~bash
	virtualenv venv
	source venv/bin/activate
	~~~

	Now you are in the virtual environment!

4. Installing the required packages. The file 	requirements.txt contains a list of them.

	~~~bash
	pip install -r Python_venv/requirements.txt
	~~~

5. Run the ipython notebook

	~~~bash
	cd Disaster_Recovery/iPythonNotebooks
	ipython notebook testing_busRescheduler.ipynb
	~~~

6. Exit the virtual environment

	~~~bash
	deactivate
	~~~
	
	In the future you do not need to install the virtual environment again, just need to activate it.
	
	
	### 



















