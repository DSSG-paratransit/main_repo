from flask import Flask, request, render_template, session
#from wtforms import Form, BooleanField, TextField, validators
import csv

app = Flask(__name__)


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
         return request.form['text']
    return render_template('my_text.html')

@app.route("/display", methods=["GET","POST"])
def preferred_options():
  # Displays a table
  if request.method == 'POST':
    data_rows = read_csv() #move this to the waiting page
    session['data_rows'] = data_rows
    session['bookingid'] = None
    session['busid'] = None
    if request.form.get('bookingid', None) is not None:
      bookingid = request.form['bookingid']
      session['bookingid'] = bookingid
    elif request.form.get('busid', None) is not None:
      busid = request.form['busid']
      session['busid'] = busid

    #check to make sure we have aws keys or a filename for demo data?
    #if session['accesskey'] and session['file'] is None:
    #   return render_template('admin.html')?
    #start waiting page
    #busRescheduler_run(filename, accesskey, secretkey, ...)

    row_range = range(len(data_rows))
    return render_template('preferred_options.html', #are bookingid, busid, etc found in request.form.get('bookingid'), etc?
        bookingid = bookingid,
        busid = busid,
        row_range = row_range,
        data_rows = data_rows, 
        last_data_row = len(data_rows) - 1,
        )

  return render_template('request.html')

@app.route("/waiting", methods = ['GET', 'POST'])
def execute():
  








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
    session['accesskey'] = None
    session['secretkey'] = None
    session['filename'] = None
    if request.form.get('accesskey', None) is not None:
      accesskey = request.form['accesskey']
      secretkey = request.form['secretkey']
    elif request.form.get('file', None) is not None:
      filename = request.form['file']
    msg = "accesskey is %s. secret key is %s. file is %s" % (
        accesskey, secretkey, filename)
    session['accesskey'] = accesskey #how do I access these when I want them?
    session['secretkey'] = secretkey
    session['file'] = filename
    return msg

  return render_template('admin.html')


if __name__ == "__main__":
  app.debug = True
  app.secret_key = 'F12Zr47j\3yX R~6@H!jmM]Lwf/,?K9'
  app.run()
