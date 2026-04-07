from .storage import write_json, read_json

def save_case_snapshot(case_id, snapshot):
    write_json(f"case_{case_id}.json", snapshot)

def load_case_snapshot(case_id):
    return read_json(f"case_{case_id}.json", default={})

def load_all_snapshots():
    # You can expand this later to scan the directory
    pass
