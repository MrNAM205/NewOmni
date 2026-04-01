from __future__ import annotations

from typing import Dict, Any

from .extractor import extract_fields
from backend.model_router.router import route_request


def handle_document(text: str, context: Dict[str, Any] | None = None):
    context = context or {}

    # 1. Extract structured fields
    fields = extract_fields(text)

    # 2. Ask model router for neutral reasoning
    model_result = route_request(
        task="analysis",
        user_input=text,
        metadata={"source": "document", **context}
    )

    # 3. Merge structured fields + reasoning
    final_output = (
        "Here’s what I can identify from this document:

"
        + _format_fields(fields)
        + "

"
        + model_result["persona_output"]
    )

    return {
        "fields": fields,
        "model": model_result["model"],
        "output": final_output
    }


def _format_fields(fields: Dict[str, Any]) -> str:
    lines = []
    for key, value in fields.items():
        if value:
            lines.append(f"- {key}: {value}")
    return "
".join(lines) if lines else "No structured fields detected."
