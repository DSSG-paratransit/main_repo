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
    data_rows = read_csv()
    session['data_rows'] = data_rows
    bookingid = None
    busid = None
    if request.form.get('bookingid', None) is not None:
      bookingid = request.form['bookingid']
      is_bus = False
    elif request.form.get('busid', None) is not None:
      busid = request.form['busid']
      is_bus = True
    row_range = range(len(data_rows))
    return render_template('preferred_options.html', 
        bookingid = bookingid,
        busid = busid,
        row_range = row_range,
        data_rows = data_rows, 
        last_data_row = len(data_rows) - 1,
        )

  return render_template('request.html')

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


if __name__ == "__main__":
  app.debug = True
  app.secret_key = 'F12Zr47j\3yX R~6@H!jmM]Lwf/,?K9'
  app.run()
