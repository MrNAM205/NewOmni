def build_primary_plan(snapshot):
    posture = snapshot["synthesis"].get("posture", [])
    timeline = snapshot.get("timeline", [])

    steps = []

    if "action required" in posture:
        steps.append("Review the latest document and confirm required response.")

    if timeline:
        next_deadline = timeline[0]
        steps.append(f"Prepare materials for deadline on {next_deadline.get('date')}.")

    steps.append("Verify all entities and reference numbers are correct.")
    steps.append("Update case memory with any new findings.")

    return steps
