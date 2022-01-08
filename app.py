from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import json
import random
import extract_data
import quote
import os



TIME_UPLOAD_FOLDER = "/home/pi/Time/FlaskTimeTracking/data/time"
ALLOWED_EXTENSIONS = {"csv", "txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = TIME_UPLOAD_FOLDER


def random_colors(n):
    colors = []
    for i in range(n):
        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        colors.append(hexadecimal)
    
    return colors

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/quote')
def quote():
    quote.update()
    with open("quotes/quote.json", "r") as jsonquote:
        data = json.load(jsonquote)

    quote  = data["quote"]
    author = data["author"]
    date = data["date"]
    return render_template("quote.html", quote=quote, author=author, date=date)


@app.route('/time', methods=['GET', 'POST'])
def today():
    
    if request.method == 'POST':
        if request.form.get('day') == 'Day':
            labels, values = extract_data.today_data()
            colors = random_colors(len(labels))
            return render_template("pie_chart.html", title="Today Graph" , values=values, labels=labels, colors=colors)
        elif request.form.get('week') == 'Week':
            labels, values = extract_data.weekly_data()
            colors = random_colors(len(labels))
            return render_template("pie_chart.html", title="Weekly Graph" , values=values, labels=labels, colors=colors)
        elif request.form.get('month') == 'Month':
            labels, values = extract_data.monthly_data()
            colors = random_colors(len(labels))
            return render_template("pie_chart.html", title="Monthly Graph" , values=values, labels=labels, colors=colors)
        else:
            print("UNKNOWN")
        
    elif request.method == 'GET':
        return render_template('pie_chart.html', title="Today Graph")


@app.route('/time/<activity>', methods=['GET', 'POST'])
def data_activity(activity):
    if request.method == 'POST':
        if request.form.get('week') == 'Week':
            labels, values = extract_data.weekly_data_activity(activity)
            return render_template("act_chart.html", title="Weekly Graph" , activity=activity, values=values, labels=labels)

        elif request.form.get('month') == 'Month':
            labels, values = extract_data.monthly_data_activity(activity)
            return render_template("act_chart.html", title="Monthly Graph" , activity=activity, values=values, labels=labels)

        else:
            print("UNKNOWN")
        
    elif request.method == 'GET':
        labels, values = extract_data.weekly_data_activity(activity)
        return render_template("act_chart.html", title="Weekly Graph" , activity=activity, values=values, labels=labels)
        #return render_template('act_chart.html', title="Graph", activity=activity)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html')
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")