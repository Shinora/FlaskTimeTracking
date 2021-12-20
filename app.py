from flask import Flask, render_template, request
import json
import random
import extract_data
import quote


def random_colors(n):
    colors = []
    for i in range(n):
        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        colors.append(hexadecimal)
    
    return colors

app = Flask(__name__)
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
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")