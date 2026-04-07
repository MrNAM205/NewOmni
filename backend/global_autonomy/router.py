from .detectors import detect_global_risks
from .aggregators import aggregate_triggers
from .posture import compute_global_posture
from .alerts import build_global_alerts

def run_global_autonomy(all_snapshots):
    risks = detect_global_risks(all_snapshots)
    triggers = aggregate_triggers(all_snapshots)
    posture = compute_global_posture(all_snapshots)
    alerts = build_global_alerts(risks, triggers, posture)

    return {
        "risks": risks,
        "triggers": triggers,
        "posture": posture,
        "alerts": alerts
    }
