from flask import json


def static_load_db():
    with open("data.json", encoding='utf-8') as f:
        return json.load(f)


