from flask import Flask, request, render_template
#from wtforms import Form, BooleanField, TextField, validators
#from flaskext.genshi import render_response

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
    rideid = None
    busid = None
    if request.form.get('rideid', None) is not None:
      rideid = request.form['rideid']
      is_bus = False
    elif request.form.get('busid', None) is not None:
      busid = request.form['busid']
      is_bus = True
    headers = ROWS[0]
    rows = ROWS[1:]
    row_range = range(len(rows))
    header_range = range(len(headers))
    return render_template('table_display.html', 
        rideid = rideid,
        busid = busid,
        parameters = row_range,
        header_range = header_range,
        row_range = row_range,
        headers = headers,
        rows = rows, 
        )

  return render_template('table_request.html')

@app.route("/link/<parameter>/<value>", methods=["GET"])
def link(parameter, value):
  return "Got to link with parameter %s and value %s" % (parameter, value)


if __name__ == "__main__":
    app.debug = True
    app.run()
