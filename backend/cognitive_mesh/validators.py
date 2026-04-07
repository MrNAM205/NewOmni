def run_validations(snapshot):
    issues = []

    # Timeline vs Mission
    mission_deadlines = snapshot["mission"]["components"]["header"]
    timeline = snapshot["timeline"]

    if timeline and "deadline" in mission_deadlines.lower():
        last = timeline[-1]
        if str(last.get("date")) not in mission_deadlines:
            issues.append({
                "type": "deadline_mismatch",
                "message": "Mission deadline does not match timeline."
            })

    # Entities vs Synthesis
    entities = snapshot["entities"]
    posture = snapshot["synthesis"].get("posture", [])

    if "financial obligations" in posture and "IRS" not in entities:
        issues.append({
            "type": "entity_missing",
            "message": "Financial posture detected but no financial entity found."
        })

    return issues
