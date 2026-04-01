# backend/ipc_handlers/scenario_handler.py

from backend.scenario_router.router import handle_scenario

def handle_scenario_ipc(payload):
    user_input = payload.get("input", "")
    context = payload.get("context", {})

    result = handle_scenario(user_input, context)

    return {
        "type": "scenario_response",
        **result
    }
