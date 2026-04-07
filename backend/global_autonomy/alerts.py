def build_global_alerts(risks, triggers, posture):
    alerts = []

    if risks:
        alerts.append({
            "type": "global_high_risk",
            "message": f"{len(risks)} cases have high-severity issues."
        })

    if any(t["trigger"].get("type") == "fallback" for t in triggers):
        alerts.append({
            "type": "fallback_wave",
            "message": "Multiple cases have activated fallback paths."
        })

    if posture.get("action_required", 0) > 3:
        alerts.append({
            "type": "action_overload",
            "message": "More than 3 cases require immediate action."
        })

    return alerts
