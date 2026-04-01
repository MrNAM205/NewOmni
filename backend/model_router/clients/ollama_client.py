# backend/model_router/clients/ollama_client.py

import time
import requests


def generate(model, user_input):
    start = time.time()

    payload = {
        "model": model["name"],
        "prompt": user_input,
    }

    r = requests.post(model["endpoint"], json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()

    text = data.get("response") or data.get("output") or str(data)
    latency_ms = int((time.time() - start) * 1000)
    return text, latency_ms
