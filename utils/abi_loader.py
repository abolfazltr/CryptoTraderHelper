import json

def load_abi(path):
    with open(path, "r") as f:
        return json.load(f)