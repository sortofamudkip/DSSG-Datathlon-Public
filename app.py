from flask import Flask, render_template

app = Flask(__name__, template_folder="./pages")


@app.route("/")
def index():
    return render_template("maps.html")
    
@app.route("/bike_stations")
def stations():
    return render_template("maps.html")


