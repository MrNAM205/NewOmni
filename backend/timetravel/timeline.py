def build_timeline(case_events, alerts, global_events):
    combined = []

    combined.extend([
        { "type": "case", **e } for e in case_events
    ])

    combined.extend([
        { "type": "alert", **a } for a in alerts
    ])

    combined.extend([
        { "type": "global", **g } for g in global_events
    ])

    combined.sort(key=lambda x: x["timestamp"])

    return combined
