from flask import Flask, render_template

from model import db

# from HarborviewProject.model import model
app = Flask(__name__)


@app.route("/")
def welcome():
    new = 123
    return render_template("welcome.html", ab=new)


@app.route("/languages")
def languages():
    languages = db
    return render_template("languages.html", language=languages)


@app.route("/screening/<int:index>")
def screening(index):
    languages = db
    questions = languages[index]
    return render_template("screening_q.html", language=questions)

# @app.route("/card/<int: index>")
# def card_view(index):
#     card = db[index]
#     return render_template("card.html", card=card)
