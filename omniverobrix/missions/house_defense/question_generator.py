# omniverobrix/missions/house_defense/question_generator.py

from typing import Dict, Any, List


class HouseDefenseQuestionGenerator:
    def generate_questions(
        self,
        summary: Dict[str, Any],
        document_groups: Dict[str, List[int]],
    ) -> Dict[str, List[str]]:
        """
        Returns:
        {
          "for_nonprofits": [...],
          "for_lawyers": [...],
          "for_county": [...],
        }
        """
        known = summary.get("known", [])
        unknown = summary.get("unknown", [])

        q_nonprofits = []
        q_lawyers = []
        q_county = []

        # Ownership gaps
        if any("No clear ownership documents" in u for u in unknown):
            q_nonprofits.append(
                "Can you help me understand what documents I need to prove ownership of the house?"
            )
            q_lawyers.append(
                "What steps are usually involved in confirming or correcting ownership of inherited property?"
            )

        # Tax gaps
        if any("No clear property tax documents" in u for u in unknown):
            q_county.append(
                "Can you provide a full history of property tax assessments and payments for this property?"
            )

        # Court/probate gaps
        if any("No clear court/probate documents" in u for u in unknown):
            q_lawyers.append(
                "Has any probate or court process already occurred that I should be aware of?"
            )

        # Timeline gaps
        if any("No dates were detected" in u for u in unknown):
            q_nonprofits.append(
                "What dates and events are most important to track for housing stability and legal issues?"
            )

        # General questions
        q_nonprofits.append(
            "Based on my situation, what programs or resources might help me keep or stabilize the house?"
        )
        q_lawyers.append(
            "Are there any deadlines or time limits I should be aware of regarding taxes, probate, or eviction?"
        )
        q_county.append(
            "What is the current status of this property in your records (owner of record, tax status, any liens)?"
        )

        return {
            "for_nonprofits": q_nonprofits,
            "for_lawyers": q_lawyers,
            "for_county": q_county,
        }
