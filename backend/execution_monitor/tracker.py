def update_step_state(state, event):
    step = event["step"]
    status = event["status"]

    state.setdefault("steps", {})
    state["steps"][step] = status

    return state
