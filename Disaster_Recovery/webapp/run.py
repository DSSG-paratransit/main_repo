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
        return render_template('request.html', error = error)

    row_range = range(len(data_rows))
    session['row_range'] = row_range
    # print(url_for('rescheduling'))


    return redirect(url_for('rescheduling'))
    

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


def clean_a_o(lst_strs):
    new_table_inds = []
    for k in range(len(lst_strs)):
      for char in lst_strs[k]:
        if char in "[]":
          lst_strs[k] = lst_strs[k].replace(char, '')
      if re.search("OPTION", lst_strs[k]): #index of list where we should make new option table
        new_table_inds.append(k)
    return lst_strs, new_table_inds


@app.route("/link/<row>", methods=["GET"])
def link(row):
    bookingid = session['data_rows'][int(row)][0]
    print(bookingid)
    bid_file = open(os.path.join('data', str(bookingid)+'_insert_data.txt'), 'r')
    bid_insert_txt, new_table_inds = clean_a_o(bid_file.readlines()) #this list of strings and a list of indices

    # present 0 - 3 alternative options on the alternative_options.html page.
    if len(bid_insert_txt) > 0:
      opt1 = bid_insert_txt[new_table_inds[0]:new_table_inds[0]+4]; print(opt1)
    else: opt1 = None
    if len(bid_insert_txt) > 5:
      opt2 = bid_insert_txt[new_table_inds[1]:new_table_inds[1]+4]; print(opt2)
    else: opt2 = None
    if len(bid_insert_txt) > 10:
      opt3 = bid_insert_txt[new_table_inds[2]:new_table_inds[2]+4]; print(opt3)
    else: opt3 = None

    return render_template('alternative_options.html', 
        bookingid = bookingid,
        opt1 = opt1, opt2 = opt2, opt3 = opt3
        num_opts = len(bid_insert_txt)/5
        )



  
@app.route("/rescheduling",methods = ["GET","POST"])
def rescheduling():

    #define command line arguments
    if session['file'] is not None:
      demo_file = os.path.join(os.getcwd(), 'data', session['file']) #need to get this from admin page later...
    else:
      demo_file = 'None'
    path_to_outdir = os.path.join(os.getcwd(),'data'); print(path_to_outdir)
    path_to_rescheduler = os.path.join('..', 'core', 'busRescheduler.py')
    args = ['python', str(path_to_rescheduler), 
    demo_file, str(session['accesskey']), str(session['secretkey']), str(session['busid']),
    path_to_outdir, str(session['beginTime']), str(session['bookingid']), '1800.', '3.']

    print args
    # removing the flag, stdout, and stderr files.
    if os.path.isfile(os.path.join('data','flag.txt')):
        os.remove(os.path.join('data','flag.txt'))
    if os.path.isfile(os.path.join('data','stdout.txt')):
        os.remove(os.path.join('data','stdout.txt'))
    if os.path.isfile(os.path.join('data','stderr.txt')):
        os.remove(os.path.join('data','stderr.txt'))

    # begin a subprocess to run busRescheduler:
    f_out = open(os.path.join('data', 'stdout.txt'), 'w')
    f_err = open(os.path.join('data', 'stderr.txt'), 'w')
    p = subprocess.Popen(args, stdout=f_out, stderr = f_err)

    session['pid'] = p.pid
    print p.pid
    return(render_template('thumbsucker.html'))
    
  

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

    if (accesskey == '' or secretkey == '') and filename is None: 
      error = 'Missing either an AWS accesskey or a secret key.'
      return render_template('admin.html', error = error)

    session['accesskey'] = accesskey; print(session['accesskey'])
    session['secretkey'] = secretkey; print(session['secretkey'])
    session['file'] = filename; print(session['file'])
    return render_template('request.html', accesskey = accesskey, secretkey = secretkey)

  return render_template('admin.html')


def check_run_errors():
  # if os.path.isfile(os.path.join('data', 'stderr.txt')):
  error_list = open(os.path.join('data', 'list_python_errortypes.txt'), 'r')
  el = error_list.readlines(); error_list.close()
  stderr = open(os.path.join('data', 'stderr.txt'), 'r')
  se = stderr.read(); stderr.close()
  for err in el:
    if re.search(err, se):
      return -1
  else:
    return 0

@app.route("/thumbsucker/", methods=["GET","POST"])
def thumbsucker():
  
  count = session.get('count', 0) + 1
  session['count'] = count

  #See if busRescheduler returned errors.
  status = check_run_errors()
  if status == -1:
    error_string = 'Run time error. Please refer to stderr.txt file.'
    return render_template('error_page.html', error_string = error_string)

  # if process still isnt completed
  if not os.path.isfile(os.path.join('data','flag.txt')):
    display_string = "Currently rerouting passengers. This may take a while (Order of 10 minutes). Please wait{0}".format("."*(count%4))
    return render_template('thumbsucker.html', display_string=display_string)

  #if process is completed...
  if os.path.isfile(os.path.join('data', 'flag.txt')):
    knownerrorfile = open(os.path.join('data', 'flag.txt'), 'r')
    flg = knownerrorfile.readlines()
    knownerrorfile.close()
    #process completed but with KNOWN busRescheduler.py flag code errors.
    if re.search('400', flg[0]):
      error_string = 'Submitted data is either incorrectly formatted, of incorrect type, or misspelled. Please revisit the display page.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('401', flg[0]):
      error_string = 'Demo file not found. Please revisit the admin page.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('402', flg[0]):
      error_string = 'Formatting of streaming data file is incorrect. Please revisit the admin page.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('403', flg[0]):
      error_string = 'Streaming data could not be accessed correctly. Please revisit the admin page and try different AWS keys.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('404', flg[0]):
      error_string = 'Requested Run number is not scheduled for today. Please revisit the display page.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('405', flg[0]):
      error_string = 'You have entered BookingIds not present in the requested schedule. Please revisit the display page.'
      return render_template('error_page.html', error_string = error_string)
    if re.search('406', flg[0]):
      error_string = 'There are no clients left to reschedule after the requested initial time. Please revisit the display page.'
      return render_template('error_page.html', error_string = error_string)

    #process completed cleanly 
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
