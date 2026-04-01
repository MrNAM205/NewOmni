from __future__ import annotations

from typing import Dict, Any

from backend.model_router.router import route_request
from .templates import detect_domain, build_procedural_outline


def handle_scenario(user_input: str, context: Dict[str, Any] | None = None):
    """
    High-level scenario interpreter.
    """
    context = context or {}

    # 1. Detect domain (traffic, billing, administrative, general)
    domain = detect_domain(user_input)

    # 2. Build procedural outline (steps, checklists, definitions)
    outline = build_procedural_outline(domain, user_input)

    # 3. Ask the model router for neutral reasoning
    model_result = route_request(
        task="analysis",
        user_input=user_input,
        metadata={"domain": domain, **context}
    )

    # 4. Merge procedural outline + model reasoning
    final_output = (
        outline
        + "

"
        + model_result["persona_output"]
    )

    return {
        "domain": domain,
        "outline": outline,
        "model": model_result["model"],
        "output": final_output
    }
