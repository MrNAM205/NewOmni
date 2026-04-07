from backend.persistence.snapshots import load_case_snapshot
from backend.persistence.alerts import load_alert_history
from backend.persistence.global_state import load_global_state

def load_case_history(case_id):
    # Later you’ll expand this to load multiple snapshots
    return load_case_snapshot(case_id)

def load_alerts():
    return load_alert_history()

def load_global_history():
    return load_global_state()
