from flask import Flask, request, render_template
#from wtforms import Form, BooleanField, TextField, validators
import csv

app = Flask(__name__)


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
         return request.form['text']
    return render_template('my_text.html')

ROWS = [("A", "B"), (1, 2), (3,4)]
@app.route("/display", methods=["GET","POST"])
def display():
  # Displays a table
  if request.method == 'POST':
    headers, data_rows = read_csv()
    bookingid = None
    busid = None
    if request.form.get('bookingid', None) is not None:
      bookingid = request.form['bookingid']
      is_bus = False
    elif request.form.get('busid', None) is not None:
      busid = request.form['busid']
      is_bus = True
    row_range = range(len(data_rows))
    header_range = range(len(headers))
    return render_template('table_display.html', 
        bookingid = bookingid,
        busid = busid,
        parameters = row_range,
        header_range = header_range,
        row_range = row_range,
        headers = headers,
        data_rows = data_rows, 
        )

  return render_template('table_request.html')

def read_csv(filename='data/preferred_options.csv'):
  # Reads data from the csv file
  # Return - headers: string of headers
  #          data_rows: list of rows corresponding to the headers
  with open(filename, 'rb') as csvfile:
      rows = csv.reader(csvfile, delimiter=',')
      data_rows = []
      got_header = False
      for row in rows:
        if not got_header:
          headers = row
          got_header = True
        else:
          data_rows.append(row)
  return headers, data_rows
  

@app.route("/link/<parameter>/<value>", methods=["GET"])
def link(parameter, value):
  return "Got to link with parameter %s and value %s" % (parameter, value)


if __name__ == "__main__":
    app.debug = True
    app.run()
