This is a web front end for the paratransit application. It is currently
in the webapp branch.

This works for python 2.7. Python 2.7.9 is recommended since it is
bundled with pip.

The application uses flask and wtforms. You can install them using:
  pip install flask
  pip install easy_install wtforms
(Note: for Mac and linux, you may need to "sudo" these commands.)

To run the application: 
  cd main_repo/Disaster_Recovery/webapp
  python run.py
  browse to http://localhost:5000/display
