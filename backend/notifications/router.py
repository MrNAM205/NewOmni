from .collector import collect_all_alerts
from .formatter import format_alerts
from .dispatcher import dispatch_alerts

def run_notifications_layer(case_snapshots, global_autonomy_output):
    raw_alerts = collect_all_alerts(case_snapshots, global_autonomy_output)
    formatted = format_alerts(raw_alerts)
    dispatchable = dispatch_alerts(formatted)

    return dispatchable
