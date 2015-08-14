from flask import Flask, request, redirect, url_for
from flask import render_template, session, make_response, flash
import re
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
    session['accesskey'] = None
    session['secretkey'] = None
    # session['file']

    #define command line arguments
    demo_file = os.path.join(os.getcwd(), 'data', session['file']) #need to get this from admin page later...
    path_to_outdir = os.path.join(os.getcwd(),'data'); print(path_to_outdir)
    path_to_rescheduler = os.path.join('..', 'core', 'busRescheduler.py')
    args = ['python', str(path_to_rescheduler), 
    demo_file, str(session['accesskey']), str(session['secretkey']), str(session['busid']),
    path_to_outdir, str(session['beginTime']), str(session['bookingid']), '1800.', '3.']
    args.append("2>"+os.path.join(path_to_outdir,'error_output.txt'))
    args.append("1>"+os.path.join(path_to_outdir, 'cmdline_output.txt'))

    print args
    # removing the flag file. Successfully implemented.
    if os.path.isfile(os.path.join('data','flag.txt')):
        os.remove(os.path.join('data','flag.txt'))
    if os.path.isfile(os.path.join('data','error_output.txt')):
        os.remove(os.path.join('data','error_output.txt'))
    if os.path.isfile(os.path.join('data','cmdline_output.txt')):
        os.remove(os.path.join('data','cmdline_output.txt'))

        
    p = subprocess.Popen(args, stdout=subprocess.PIPE)

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
    return render_template('request.html')

  return render_template('admin.html')

@app.route("/thumbsucker/", methods=["GET","POST"])
def thumbsucker():
  
  count = session.get('count', 0) + 1
  session['count'] = count

  #if there's an error_output file, display it
  if os.path.isfile(os.path.join('error_output.txt')):
    error_file = open(os.path.join('data', 'error_output.txt'), 'r')
    error_string = error_file.readlines()[0]
    return render_template('error_page.html', error_string = error_string)
  
  # if process still isnt completed
  if not os.path.isfile(os.path.join('data','flag.txt')):
    display_string = "Still re-routing passengers. Looping %d times." % count
    return render_template('thumbsucker.html', display_string=display_string)

  #if process is completed...
  if os.path.isfile(os.path.join('data', 'flag.txt')):
    errorfile = open(os.path.join('data', 'flag.txt'), 'r')
    flg = errorfile.readlines()
    #process completed but with errors
    if re.search('200', flg[0]):
      error_string = 'There Error in your request. Please check to see if your Run number and/or booking IDs are valid and that they were previously scheduled for today. It is also possible that you have entered a time at which a bus has no more remaining passengers. Please go back to the display page.'
      return render_template('error_page.html', error_string = error_string)
    #process completed cleanly 
    elif os.path.isfile(os.path.join('data', 'flag.txt')):
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
