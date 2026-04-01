# backend/ipc_handlers/ask_handler.py

from backend.model_router.router import route_request

def handle_ask(payload):
    task = payload.get("task", "reasoning")
    user_input = payload.get("input", "")
    context = payload.get("context", {})

    result = route_request(task, user_input, metadata=context)

    # The router already returns the full dictionary, so we just add the type
    # and return it.
    return {
        "type": "ask_response",
        **result
    }
