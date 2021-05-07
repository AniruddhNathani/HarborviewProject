from flask import Flask, render_template, request
from model import load_db, response

# from HarborviewProject.model import model
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")


@app.route("/languages", methods=["GET", "POST"])
def languages():
    db = load_db()
    response_list = response()
    return render_template("languages.html", language=db, response_list=response_list)


@app.route("/lang_index=<int:index>/screening/screening_one", methods=["GET", "POST"])
def screening_one(index):
    db = load_db()
    language = db[index]
    return render_template("screening_one.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_two", methods=["GET", "POST"])
def screening_two(index):
    db = load_db()
    language = db[index]
    return render_template("screening_two.html", language=language)

