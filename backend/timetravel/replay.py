def replay_case(case_history):
    timeline = []

    for snapshot in case_history.get("history", []):
        timeline.append({
            "timestamp": snapshot["timestamp"],
            "posture": snapshot["posture"],
            "steps": snapshot["steps"],
            "triggers": snapshot.get("triggers", [])
        })

    return timeline
