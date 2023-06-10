import json
from typing import Dict


def load_config() -> Dict:
    with open('secrets/firebase.json', 'r') as file:
        firebase_config = json.load(file)
    return firebase_config
