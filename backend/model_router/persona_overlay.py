# backend/model_router/persona_overlay.py

from __future__ import annotations

from typing import Any, Dict


def apply_persona(text: str, context: Dict[str, Any] | None = None) -> str:
    """
    Wrap raw model output in the OmniVerobrix / Sir Robert persona.

    This is intentionally simple for v1:
    - stabilizes tone
    - adds light framing
    - keeps content intact

    Later we can:
    - inject mission headers
    - add risk flags
    - add next-step suggestions
    - adapt tone by scenario
    """
    context = context or {}
    task = context.get("task", "reasoning")
    model = context.get("model", "sovereign-router")

    core_voice_prefix = (
        "Staying in sovereign, cockpit-grade mode. "
        "Here’s my response, grounded and operational:\n\n"
    )

    # Optional: light task-aware framing
    if task == "coding":
        framing = "I’ll keep this tight, practical, and implementation-focused.\n\n"
    elif task == "summarization":
        framing = "Here’s a distilled, high-signal summary:\n\n"
    elif task == "analysis":
        framing = "Here’s a structured breakdown of what matters:\n\n"
    else:
        framing = ""

    # You can also log or tag the model here if you want:
    model_tag = f"[model: {model}]\n\n"

    # v1: keep it simple and non-intrusive
    return f"{core_voice_prefix}{framing}{text.strip()}"
