from flask import Flask, render_template
import json


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quote')
def quote():
    with open("quotes/quote.json", "r") as jsonquote:
        data = json.load(jsonquote)
        
    quote  = data["quote"]
    author = data["author"]
    date = data["date"]
    return render_template("quote.html", quote=quote, author=author, date=date)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")