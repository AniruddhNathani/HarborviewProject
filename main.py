from flask import Flask, render_template, request, session
import model as md
# from flask_session import Session
import os
from pathlib import Path
from flask_session import Session
from collections import defaultdict

# from HarborviewProject.model import model
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.secret_key = 'BAD_SECRET_KEY'


@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")


@app.route("/languages", methods=["GET", "POST"])
def languages():
    db = md.static_load_db()
    session.clear()
    session["response_list"] = dict(defaultdict())
    session["flag"] = 0
    return render_template("languages.html", language=db)


@app.route("/lang_index=<int:index>/screening/screening_one", methods=["GET", "POST"])
def screening_one(index):
    db = md.static_load_db()
    language = db[index]
    return render_template("screening_one.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_two", methods=["GET", "POST"])
def screening_two(index):
    db = md.static_load_db()
    language = db[index]
    if request.method == "POST":
        if request.form.get("yes_button"):
            session["response_list"]["screen_one"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_one"] = "no"
    return render_template("screening_two.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/final_response", methods=["GET", "POST"])
def final_response(index):
    if request.method == "POST":
        if request.form.get("yes_button"):
            session["response_list"]["screen_two"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_two"] = "no"

    for key, value in session["response_list"].items():
        if value == "yes":
            session["flag"] = 1
            break
        else:
            session["flag"] = 0
    print(session["response_list"], session["flag"])
    return render_template("final_response.html")


@app.route("/patient-responses")
def patient_response():
    base_path = Path(os.getcwd()+"/flask_session")

    list_of_files = {}
    for filename in os.listdir(base_path):
        fn = base_path.joinpath(filename)
        with open(fn) as f:
            list_of_files[filename] = f.read()

    return render_template("patient_responses.html", response=list_of_files)


if __name__ == "__main__":
    app.run()