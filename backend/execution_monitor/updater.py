def update_mission_posture(state):
    steps = state.get("steps", {})
    completed = [s for s, v in steps.items() if v == "completed"]
    pending = [s for s, v in steps.items() if v != "completed"]

    if not completed:
        return "action required"

    if pending:
        return "in progress"

    return "completed"
