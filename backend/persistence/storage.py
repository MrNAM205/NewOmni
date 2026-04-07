import json
import os

BASE_DIR = "data"

def ensure_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def write_json(path, data):
    ensure_dir()
    with open(os.path.join(BASE_DIR, path), "w") as f:
        json.dump(data, f, indent=2)

def read_json(path, default=None):
    try:
        with open(os.path.join(BASE_DIR, path), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
