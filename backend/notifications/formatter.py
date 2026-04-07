def format_alerts(alerts):
    formatted = []

    for a in alerts:
        formatted.append({
            "scope": a.get("scope", "unknown"),
            "case_id": a.get("case_id"),
            "type": a["type"],
            "message": a["message"],
            "priority": compute_priority(a)
        })

    return formatted


def compute_priority(alert):
    if alert["type"] in ("global_high_risk", "fallback_wave"):
        return "high"
    if alert["type"] in ("blocked", "fallback"):
        return "medium"
    return "low"
