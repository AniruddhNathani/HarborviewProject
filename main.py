from flask import Flask, render_template, request, session, json
import model as md
from flask_session import Session
from collections import defaultdict


app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.secret_key = 'BAD_SECRET_KEY'
# global response_list
# global session_language


@app.route("/", methods=["GET", "POST"])
def welcome():
    session.clear()
    session["response_list"] = dict(defaultdict())
    session["flag"] = 0
    session["triage_flag"] = 0
    session["language"] = ''

    return render_template("welcome.html")


@app.route("/languages", methods=["GET", "POST"])
def languages():

    db = md.static_load_db()
    return render_template("languages.html", language=db)


@app.route("/lang_index=<int:index>/screening/screening_one", methods=["GET", "POST"])
def screening_one(index):
    db = md.static_load_db()
    language = db[index-1]
    return render_template("screening_one.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_two", methods=["GET", "POST"])
def screening_two(index):
    db = md.static_load_db()
    language = db[index-1]

    if request.method == "POST":
        session["language"] = language["trns_name"]
        if request.form.get("yes_button"):
            session["response_list"]["screen_one"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_one"] = "no"
    return render_template("screening_two.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_three", methods=["GET", "POST"])
def screening_three(index):
    db = md.static_load_db()
    language = db[index-1]

    if request.method == "POST":
        session["language"] = language["trns_name"]
        if request.form.get("yes_button"):
            session["response_list"]["screen_two"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_two"] = "no"
    return render_template("screening_three.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/screening_four", methods=["GET", "POST"])
def screening_four(index):
    db = md.static_load_db()
    language = db[index-1]

    if request.method == "POST":
        session["language"] = language["trns_name"]
        if request.form.get("yes_button"):
            session["response_list"]["screen_three"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_three"] = "no"
    return render_template("screening_four.html", language=language, index=index)


@app.route("/lang_index=<int:index>/screening/final_response", methods=["GET", "POST"])
def final_response(index):
    db = md.static_load_db()
    language = db[index - 1]

    if request.method == "POST":
        if request.form.get("yes_button"):
            session["response_list"]["screen_four"] = "yes"
        elif request.form.get("no_button"):
            session["response_list"]["screen_four"] = "no"

    for key, value in session["response_list"].items():
        if key in ["screen_one", "screen_two"]:
            if value == "yes":
                session["flag"] = 1
                break
            else:
                session["flag"] = 0
        if key in ["screen_four"]:
            if value == "yes":
                session["triage_flag"] = 1
            else:
                session["triage_flag"] = 0


    response_dict = {"response_list": session["response_list"], "flag": session["flag"], "language": session["language"], "triage_flag": session["triage_flag"]}
    response_file = open("response_store.json", "w", encoding='utf-8')
    json.dump(response_dict, response_file)
    response_file.close()
    return render_template("final_response.html", language=language)


@app.route("/patient-responses")
def patient_response():

    response_file = open("response_store.json", "r", encoding='utf-8')
    response_dict = json.load(response_file)

    if response_dict["response_list"]:
        response_list = response_dict["response_list"]
    else:
        response_list = []

    if response_dict["language"]:
        session_flag = response_dict["flag"]
    else:
        session_flag = 0

    if response_dict["language"]:
        session_language = response_dict["language"]
    else:
        session_language = ''

    if response_dict["triage_flag"]:
        session_triage_flag = response_dict["triage_flag"]
    else:
        session_triage_flag = 0

    response_file.close()
    return render_template("patient_responses.html", response=json.loads(json.dumps(response_list)), lang=session_language, session_flag=session_flag, triage_flag=session_triage_flag)


@app.route("/back-office-languages", methods=["GET", "POST"])
def back_office_languages():
    db = md.static_load_db()
    return render_template("back_office_languages.html", language=db)


@app.route("/lang_index=<int:index>/back-office-videos", methods=["GET", "POST"])
def back_office(index):
    db = md.static_load_db()
    language = db[index - 1]
    return render_template("back_office.html", language=language)


if __name__ == "__main__":
    app.run()
