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
        persona = self.get_persona()
        tone = persona["tone"]

        if "plain-language" in tone:
            return text

        if "precise" in tone:
            return text.replace("maybe", "possibly").replace("I think", "The evidence suggests")

        if "confident" in tone:
            return text.replace("might", "will").replace("could", "can")

        return text

    def apply_summary_style(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        persona = self.get_persona()
        style = persona["summary_style"]

        if style == "gentle, clear, focused on understanding":
            return summary

        if style == "structured, bullet-point, analytical":
            summary["summary_text"] = (
                "ANALYST SUMMARY:\n"
                f"- {summary['summary_text']}\n"
                f"- Known: {len(summary['known'])} items\n"
                f"- Unknown: {len(summary['unknown'])} items"
            )
            return summary

        if style == "persuasive, polished, outward-facing":
            summary["summary_text"] = (
                "REPRESENTATIVE SUMMARY:\n"
                f"{summary['summary_text']}\n"
                "This summary is prepared for external communication."
            )
            return summary

        return summary

    # ---------------------------------------------------------
    # High-level response shaping
    # ---------------------------------------------------------

    def shape_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies persona tone + summary style to mission outputs.
        """
        persona = self.get_persona()

        # Shape mission summaries
        if response.get("type") == "house_defense":
            result = response.get("result", {})
            summary = result.get("summary", {})

            summary = self.apply_summary_style(summary)
            summary["summary_text"] = self.apply_tone(summary["summary_text"])

            result["summary"] = summary
            response["result"] = result

        return response
