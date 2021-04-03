from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def welcome():
    return render_template("welcome.html", x=42)