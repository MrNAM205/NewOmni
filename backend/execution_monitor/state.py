STATE = {}

def load_state(case_id):
    return STATE.get(case_id, {})

def save_state(case_id, state):
    STATE[case_id] = state
