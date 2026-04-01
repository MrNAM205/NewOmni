# backend/model_router/registry.py

import json
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "models.json"

def load_models():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)
