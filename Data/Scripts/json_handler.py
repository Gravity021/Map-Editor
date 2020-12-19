import json

def load(path):
    file = open(path)
    data = json.loads(file.read())
    file.close()
    return data