import json

def read(file):
    try:
        with open(f'json/{file}', 'r', encoding="utf-8") as f:
            data = json.load(f)
            try:
                return data
            except OSError:
                return 'Cannot read data!'
    except FileNotFoundError:
        return 'File not found!'

def write(file, value):
    try:
        with open(f'json/{file}', 'w', encoding="utf-8") as f:
            json.dump(value, f)
    except FileNotFoundError:
        return 'File not found!'
