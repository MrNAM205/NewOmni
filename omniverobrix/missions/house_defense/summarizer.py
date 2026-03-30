# omniverobrix/missions/house_defense/summarizer.py

import sqlite3
from typing import Dict, Any, List


class HouseDefenseSummarizer:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def build_summary(
        self,
        mission_id: int,
        document_groups: Dict[str, List[int]],
        timeline_events: List[Dict[str, Any]],
        entities: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Returns:
        {
          "summary_text": "...",
          "known": [...],
          "unknown": [...]
        }
        """
        ownership_docs = document_groups.get("ownership", [])
        tax_docs = document_groups.get("taxes", [])
        court_docs = document_groups.get("court", [])

        known = []
        unknown = []

        if ownership_docs:
            known.append("There are documents related to ownership (deeds/titles).")
        else:
            unknown.append("No clear ownership documents were detected (deeds/titles).")

        if tax_docs:
            known.append("There are documents related to property taxes.")
        else:
            unknown.append("No clear property tax documents were detected.")

        if court_docs:
            known.append("There are documents related to court or probate.")
        else:
            unknown.append("No clear court/probate documents were detected.")

        if timeline_events:
            known.append("A timeline of events has been extracted from the documents.")
        else:
            unknown.append("No dates were detected to build a timeline.")

        people = [e["entity"] for e in entities if e["entity_type"] == "person"]
        if people:
            known.append(f"People mentioned include: {', '.join(sorted(set(people)))}.")
        else:
            unknown.append("No specific people were clearly identified in the documents.")

        summary_text = (
            "This mission focuses on understanding the situation around the house. "
            "The system has grouped documents into ownership, taxes, court, family, and unknown. "
            "It has also attempted to build a timeline and identify key people."
        )

        return {
            "summary_text": summary_text,
            "known": known,
            "unknown": unknown,
        }
