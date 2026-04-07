def dispatch_alerts(alerts):
    dispatchable = []

    for alert in alerts:
        if alert["priority"] == "high":
            dispatchable.append(alert)
        elif alert["priority"] == "medium":
            dispatchable.append(alert)
        # low priority alerts may be logged but not pushed

    return dispatchable
