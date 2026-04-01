from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from .registry import load_models
from .persona_overlay import apply_persona
from .capability_map import CAPABILITY_WEIGHTS
from .clients import (
    ollama_client,
    lmstudio_client,
    huggingface_client,
    openai_compatible_client,
)

logger = logging.getLogger(__name__)


class ModelRouterError(Exception):
    pass


_cache = {}  # (task, input) -> text  (v1: in-memory)

def _get_cached(task: str, user_input: str) -> Optional[str]:
    key = (task, user_input.strip())
    return _cache.get(key)

def _set_cached(task: str, user_input: str, output: str) -> None:
    key = (task, user_input.strip())
    _cache[key] = output


def route_request(
    task: str,
    user_input: str,
    *,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Main entry point for the Model Router Organ.

    Args:
        task: high-level intent, e.g. "reasoning", "coding", "summarization".
        user_input: raw text from the user or upstream organ.
        metadata: optional context (session id, user id, scenario, etc.).

    Returns:
        Dict with unified response structure:
        {
          "model": "<model_name>|None",
          "raw_output": "<model text>",
          "persona_output": "<wrapped text>",
          "latency_ms": <int or None>,
          "meta": {...}
        }
    """
    metadata = metadata or {}

    # Tier 3 (pre-check): cache
    cached = _get_cached(task, user_input)
    if cached:
        persona_output = apply_persona(
            cached,
            context={"task": task, "model": "cache", **metadata},
        )
        return {
            "model": "cache",
            "raw_output": cached,
            "persona_output": persona_output,
            "latency_ms": 0,
            "meta": {"task": task, "fallback": False, "from_cache": True},
        }

    models = load_models()
    candidates = _find_candidates(models, task)

    if not candidates:
        logger.warning("No candidates found for task=%s", task)
        text = "No suitable models are registered for this kind of task."
        persona_text = apply_persona(text, context=metadata or {})
        return {
            "model": None,
            "raw_output": text,
            "persona_output": persona_text,
            "latency_ms": None,
            "meta": {"task": task, "fallback": True},
        }

    last_error: Optional[Exception] = None

    for model in candidates:
        name = model.get("name")
        try:
            logger.info("Trying model=%s for task=%s", name, task)
            raw_output, latency_ms = _call_model(model, user_input)
            if not raw_output:
                raise ModelRouterError(f"Empty response from model={name}")

            persona_output = apply_persona(
                raw_output,
                context={
                    "task": task,
                    "model": name,
                    **(metadata or {}),
                },
            )
            
            _set_cached(task, user_input, raw_output)
            return {
                "model": name,
                "raw_output": raw_output,
                "persona_output": persona_output,
                "latency_ms": latency_ms,
                "meta": {
                    "task": task,
                    "fallback": False,
                },
            }

        except Exception as e:
            last_error = e
            logger.warning("Model %s failed: %s", name, repr(e))
            continue

    # All models failed → sovereign fallback
    logger.error("All models failed for task=%s; last_error=%r", task, last_error)
    fallback_text = (
        "Every available model endpoint failed or timed out. "
        "I can’t safely generate a detailed answer right now, "
        "but here’s how I’d suggest you proceed:\n\n"
        "- Pause and capture the key facts of your situation in writing.\n"
        "- Note any dates, amounts, names, and reference numbers.\n"
        "- If this involves court, bills, or official notices, keep copies of everything.\n"
        "- When systems are stable again, we can walk through this step-by-step."
    )
    persona_output = apply_persona(
        fallback_text,
        context={"task": task, **(metadata or {})},
    )

    return {
        "model": None,
        "raw_output": fallback_text,
        "persona_output": persona_output,
        "latency_ms": None,
        "meta": {
            "task": task,
            "fallback": True,
            "error": repr(last_error) if last_error else None,
        },
    }


def _score_model(model, task):
    """
    Score a model based on how well its capabilities match the task.
    """
    capabilities = model.get("capabilities", [])
    weights = CAPABILITY_WEIGHTS.get(task, {})

    score = 0.0
    for cap in capabilities:
        score += weights.get(cap, 0)

    # Add priority bias (lower priority = higher score)
    priority = model.get("priority", 999)
    score += max(0, 5 - priority) * 0.1

    # Add tier bias (local > cloud)
    tier = model.get("tier", 2)
    if tier == 1:
        score += 0.5

    return score


def _find_candidates(models: Dict[str, Any], task: str) -> List[Dict[str, Any]]:
    candidates = []

    for group in ["local", "cloud_free"]:
        for name, model in models.get(group, {}).items():
            capabilities = model.get("capabilities", [])
            if task in capabilities or "general" in capabilities:
                m = dict(model)
                m["name"] = name
                m["group"] = group
                m["tier"] = 1 if group == "local" else 2
                m["score"] = _score_model(m, task)
                candidates.append(m)

    candidates.sort(key=lambda m: m["score"], reverse=True)
    return candidates


def _call_model(model: Dict[str, Any], user_input: str) -> Tuple[str, Optional[int]]:
    """
    Dispatch to the correct client based on model['type'].
    Returns (text, latency_ms).
    """
    model_type = model.get("type")

    if model_type == "ollama":
        return ollama_client.generate(model, user_input)

    if model_type == "lmstudio":
        return lmstudio_client.generate(model, user_input)

    if model_type == "huggingface":
        return huggingface_client.generate(model, user_input)

    if model_type == "openai_compatible":
        return openai_compatible_client.generate(model, user_input)

    raise ModelRouterError(f"Unknown model type: {model_type}")
