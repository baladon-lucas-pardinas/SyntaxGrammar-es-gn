import json

def fetch_syntactic_transfer_rules(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)