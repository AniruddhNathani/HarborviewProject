import json


def load_db():
    with open("data.json") as f:
        return json.load(f)


def response():
    response_list = ["Hi"]
    return response_list


db = load_db()
