from flask import Flask, request, redirect, url_for
from flask import render_template, session, make_response, flash
import csv
import time
import subprocess
import pickle
import os

app = Flask(__name__)


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
         return request.form['text']
    return render_template('my_text.html')

@app.route("/display", methods=["GET","POST"])
def preferred_options():
  # Displays a table
  error = None
  if request.method == 'POST':
    data_rows = read_csv() #we wont have preferred_options.csv available yet...
    session['data_rows'] = data_rows
    
    #initialize variables
    session['beginTime'] = None; beginTime = session['beginTime']
    session['busid'] = None; busid = session['busid']
    session['bookingid'] = None; bookingid = session['bookingid']

    if request.form.get('bookingid', None) is not None: #booking id is filled
      bookingid = request.form['bookingid']
      session['bookingid'] = bookingid
      
    if request.form.get('busid', None) is not None and request.form.get('beginTime',None) is not None: #busid, beginTime boxes are filled
      busid = request.form['busid']
      beginTime = request.form['beginTime']
      session['busid'] = busid
      session['beginTime'] = beginTime

    #if bookingid is empty (so, case is brokenbus), and either busid or beginTime are missing from second block
    if (busid == '' or beginTime == '') and bookingid is None: 
        error = 'Missing either broken bus ID or an initial rescheduling time.'
        print('cond block 3')
        return render_template('request.html', error = error)

    row_range = range(len(data_rows))
    session['row_range'] = row_range
    # print(url_for('rescheduling'))



    return redirect(url_for('rescheduling'))
    
    # return render_template('rescheduling.html')
    # return render_template('preferred.html')
    #    bookingid = bookingid,
    #    beginTime = beginTime,
    #    busid = busid,
    #    row_range = row_range,
    #    data_rows = data_rows, 
    #    last_data_row = len(data_rows) - 1,
    #    )

  return render_template('request.html', error = None) 
  

def read_csv(filename='data/preferred_options.csv'):
  
  # Reads data from the csv file
  # Return - data_rows: list of rows corresponding to the headers
  with open(filename, 'rb') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    data_rows = []
    got_header = False
    for row in rows:
      if not got_header:
        got_header = True
      else:
        data_rows.append(row)
  return data_rows
  
@app.route("/rescheduling",methods = ["GET","POST"])
def rescheduling():


    ### variables to use
    # session['bookingid']
    # session['accesskey']
    # session['secretkey']
    # session['file']
    
    # function input(AWS keys, runID, path,bookingID)
    # call code in a subprocess
    #subprocess.check_call(['python', 'busReschedule_run', '{0}'.format(session['file']), 'session['accesskey']', session['secretkey'],
    #                 session['bookingid'], session['broken_run'], windows = 1800., session['beginTime'],
    #                 './data', radius = 3.]) 
    # ^^ subprocess.call("python_script.py",arguments) ^^
    # return output
    # if finished
    # f = open('pickled_process','w')
    
    
    # removing the flag file
    if os.path.isfile(os.path.join('data','flag.txt')):
        os.remove(os.path.join('data','flag.txt'))
        
    p = subprocess.Popen('python script.py',shell=True,
            stdout=subprocess.PIPE)
    # pickle.dump(subprocess.Popen('python script.py',shell=True,
    #        stdout=subprocess.PIPE),f)
    session['pid'] = p.pid
    print p.pid
    return(render_template('thumbsucker.html'))
    
    

  

@app.route("/link/<row>", methods=["GET"])
def link(row):
    bookingid = session['data_rows'][int(row)][0]
    return render_template('alternative_options.html', 
        bookingid = bookingid,
        )

@app.route("/admin", methods=["GET","POST"])
def admin():
  # Displays a table
  if request.method == 'POST':
    accesskey = None
    secretkey = None
    filename = None
    if request.form.get('accesskey', None) is not None:
      accesskey = request.form['accesskey']
      secretkey = request.form['secretkey']
    elif request.form.get('file', None) is not None:
      filename = request.form['file']
    msg = "accesskey is %s. secret key is %s. file is %s" % (
        accesskey, secretkey, filename)
    session['accesskey'] = accesskey
    session['secretkey'] = secretkey
    session['file'] = filename
    return msg

  return render_template('admin.html')

@app.route("/thumbsucker/", methods=["GET","POST"])
def thumbsucker():
  
  count = session.get('count', 0) + 1
  session['count'] = count
  
  # this will work only on linux I think
  # exists = os.path.exists("/proc/"+str(session['pid']))
  
  def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
    
  

  # if check_pid(session['pid']):
  if not os.path.isfile(os.path.join('data','flag.txt')):
    display_string = "Looped %d times." % count
    return render_template('thumbsucker.html', display_string=display_string)
  else:
    data_rows = read_csv('data/preferred_options.csv')
    session['data_rows'] = data_rows
    row_range = range(len(data_rows))
    return(render_template("preferred_options.html",    
        bookingid = session['bookingid'],
        beginTime = session['beginTime'],
        busid = session['busid'],
        row_range = session['row_range'],
        data_rows = session['data_rows'], 
        last_data_row = len(session['data_rows']) - 1,))


if __name__ == "__main__":
  app.debug = True
  app.secret_key = 'F12Zr47j\3yX R~6@H!jmM]Lwf/,?K9'
  app.run()
