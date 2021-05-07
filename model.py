import json


def load_db():
    with open("data.json") as f:
        return json.load(f)


def response():
    temp_list = ["fuck off"]
    return temp_list


db = load_db()
