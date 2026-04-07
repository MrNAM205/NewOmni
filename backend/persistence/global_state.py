from .storage import write_json, read_json

GLOBAL_STATE_FILE = "global_state.json"

def save_global_state(state):
    write_json(GLOBAL_STATE_FILE, state)

def load_global_state():
    return read_json(GLOBAL_STATE_FILE, default={})
