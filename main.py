from flask import Flask, render_template, request, session
from model import load_db
from flask_session import Session


# from HarborviewProject.model import model
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")


@app.route("/languages", methods=["GET", "POST"])
def languages():
    db = load_db()
    session["response_list"] = []
    return render_template("languages.html", language=db)


@app.route("/lang_index=<int:index>/screening/screening_one", methods=["GET", "POST"])
def screening_one(index):
    db = load_db()
    language = db[index]
    session["response_list"].append(["Bye"])
    return render_template("screening_one.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_two", methods=["GET", "POST"])
def screening_two(index):
    db = load_db()
    language = db[index]
    session["response_list"].append(["Bye 2"])
    print(session["response_list"])
    return render_template("screening_two.html", language=language)


if __name__ == "__main__":
    app.run()