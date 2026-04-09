import os
import subprocess
from typing import Dict, Any

from omniverobrix.core.reasoning_loop import ReasoningLoop

# Adjust this if your DB path ever moves
DB_PATH = r"C:\Users\Sir\Desktop\NewOmni\omniverobrix\omniverobrix.db"


def run_ollama(model: str, prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8", errors="ignore")


def classify_intent(prompt: str) -> str:
    classification_prompt = f"""
You are an intent classifier for a sovereign cockpit.

Classify the user's request into ONE of these categories:
- reasoning   (multi-step thinking, analysis, planning, legal/house issues)
- structured  (JSON, code, tools, schemas, configs)
- conversational (chat, rewriting, explaining, creative)
- utility     (short answers, quick facts, tiny tasks)

Respond with ONLY the category word.

User request:
\"\"\"{prompt}\"\"\"
"""
    raw = run_ollama("stablelm-1.6b", classification_prompt).strip().lower()
    if "reason" in raw:
        return "reasoning"
    if "struct" in raw:
        return "structured"
    if "convers" in raw:
        return "conversational"
    if "util" in raw:
        return "utility"
    return "reasoning"


def route_to_model(prompt: str, intent: str) -> str:
    if intent == "reasoning":
        return run_ollama("phi3-mini", prompt)
    if intent == "structured":
        return run_ollama("qwen15", prompt)
    if intent == "conversational":
        return run_ollama("gemma-2b", prompt)
    return run_ollama("stablelm-1.6b", prompt)


def route_with_reasoning_loop(prompt: str) -> Dict[str, Any]:
    rl = ReasoningLoop(db_path=DB_PATH)
    return rl.handle_query(prompt)


def route(prompt: str) -> Dict[str, Any]:
    """
    Sovereign brainstem:
    - classify intent
    - decide whether to use raw model routing or full reasoning loop
    - return a structured response dict
    """
    intent = classify_intent(prompt)

    # Anything that smells like search / missions / house / docs → reasoning loop
    if any(k in prompt.lower() for k in [
        "timeline", "entities", "ingest", "scan",
        "house", "home", "property", "mission", "remedy",
        "search", "document", "probate", "tax"
    ]):
        result = route_with_reasoning_loop(prompt)
        return {
            "source": "reasoning_loop",
            "intent": intent,
            "payload": result,
        }

    # Otherwise, pure model routing
    text = route_to_model(prompt, intent)
    return {
        "source": "models",
        "intent": intent,
        "text": text,
    }


if __name__ == "__main__":
    print(f"[OmniVerobrix Router] Using DB at: {DB_PATH}")
    while True:
        try:
            user_input = input("omniverobrix >>> ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip().lower() in {"exit", "quit"}:
            break

        result = route(user_input)
        if result.get("source") == "models":
            print(result.get("text", "").strip())
        else:
            print(result)
