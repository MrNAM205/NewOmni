# omniverobrix/persona/engine.py

from typing import Dict, Any
from omniverobrix.persona.personas import PERSONAS

class PersonaEngine:
    """
    Phase 3 Persona Engine:
    - Loads persona definitions
    - Applies tone, summary style, and risk posture
    - Shapes responses from mission modules and reasoning loop
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.active_persona = "private_individual"

    # ---------------------------------------------------------
    # Persona selection
    # ---------------------------------------------------------

    def set_persona(self, persona_name: str):
        if persona_name not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona_name}")
        self.active_persona = persona_name

    def get_persona(self) -> Dict[str, Any]:
        return PERSONAS[self.active_persona]

    # ---------------------------------------------------------
    # Response shaping
    # ---------------------------------------------------------

    def apply_tone(self, text: str) -> str:
        if not isinstance(text, str):
            return text
            
        persona = self.get_persona()
        tone = persona.get("tone", "plain-language")

        if "plain-language" in tone:
            return text

        if "precise" in tone:
            return text.replace("maybe", "possibly").replace("I think", "The evidence suggests")

        if "confident" in tone:
            return text.replace("might", "will").replace("could", "can")

        return text

    def apply_summary_style(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        persona = self.get_persona()
        style = persona.get("summary_style", "")

        if not isinstance(summary, dict):
            return summary

        if style == "gentle, clear, focused on understanding":
            return summary

        if style == "structured, bullet-point, analytical":
            if "summary_text" in summary:
                text = summary["summary_text"]
                known = len(summary.get("known", []))
                unknown = len(summary.get("unknown", []))
                summary["summary_text"] = (
                    "ANALYST SUMMARY:\n"
                    f"- {text}\n"
                    f"- Known: {known} items\n"
                    f"- Unknown: {unknown} items"
                )
            return summary

        if style == "persuasive, polished, outward-facing":
            if "summary_text" in summary:
                text = summary["summary_text"]
                summary["summary_text"] = (
                    "REPRESENTATIVE SUMMARY:\n"
                    f"{text}\n"
                    "This summary is prepared for external communication."
                )
            return summary

        return summary

    # ---------------------------------------------------------
    # High-level response shaping
    # ---------------------------------------------------------

    def _apply_tone_recursively(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._apply_tone_recursively(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._apply_tone_recursively(item) for item in data]
        elif isinstance(data, str):
            return self.apply_tone(data)
        return data

    def shape_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies persona tone + summary style to mission outputs. Never crashes on missing keys.
        """
        if not isinstance(response, dict):
            return response

        if response.get("type") == "house_defense":
            result = response.get("result", {})
            if isinstance(result, dict):
                summary = result.get("summary")
                result["summary"] = self.apply_summary_style(summary)
                response["result"] = result

        return self._apply_tone_recursively(response)
