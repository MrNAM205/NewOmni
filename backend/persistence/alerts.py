from .storage import read_json, write_json

ALERTS_FILE = "alerts.json"

def append_alerts(alerts):
    existing = read_json(ALERTS_FILE, default=[])
    existing.extend(alerts)
    write_json(ALERTS_FILE, existing)

def load_alert_history():
    return read_json(ALERTS_FILE, default=[])
