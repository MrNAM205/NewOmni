def collect_all_alerts(case_snapshots, global_autonomy):
    alerts = []

    # Case-level alerts
    for snap in case_snapshots:
        for trig in snap.get("execution", {}).get("triggers", []):
            alerts.append({
                "scope": "case",
                "case_id": snap["case_id"],
                "type": trig["type"],
                "message": trig["message"]
            })

    # Global alerts
    for alert in global_autonomy.get("alerts", []):
        alerts.append({
            "scope": "global",
            "type": alert["type"],
            "message": alert["message"]
        })

    return alerts
