import json

def load_abi(path):
    with open(path) as f:
        return json.load(f)