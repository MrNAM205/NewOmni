def check_triggers(state, action_plan):
    triggers = []

    # If a step fails, activate fallback
    for step, status in state.get("steps", {}).items():
        if status == "failed":
            triggers.append({
                "type": "fallback",
                "message": "A step failed. Activating fallback path."
            })

    # If dependencies are blocked
    for dep in action_plan.get("dependencies", []):
        if state["steps"].get(dep["depends_on"]) != "completed":
            triggers.append({
                "type": "blocked",
                "message": f"Step blocked: {dep['step']}"
            })

    return triggers
