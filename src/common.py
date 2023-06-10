import json


def load_config():
    with open('secrets/firebase.json', 'r') as file:
        firebase_config = json.load(file)
    return firebase_config
