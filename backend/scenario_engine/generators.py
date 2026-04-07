def generate_branches(snapshot):
    timeline = snapshot.get("timeline", [])
    posture = snapshot.get("synthesis", {}).get("posture", [])

    return [
        {"type": "best_case", "assumptions": ["no delays", "full compliance"]},
        {"type": "expected_case", "assumptions": ["normal processing"]},
        {"type": "worst_case", "assumptions": ["delays", "missing documents"]},
        {"type": "risk_case", "assumptions": ["supervisor issues escalate"]},
    ]
