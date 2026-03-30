# omniverobrix/missions/house_defense/document_classifier.py

import sqlite3
from typing import Dict, List


CATEGORIES = {
    "ownership": ["deed", "title", "ownership", "grantor", "grantee"],
    "taxes": ["tax", "assessment", "property tax", "delinquent", "collector"],
    "court": ["court", "hearing", "case", "docket", "probate", "judge"],
    "family": ["father", "mother", "uncle", "aunt", "heir", "beneficiary"],
}


class HouseDocumentClassifier:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def classify_mission_documents(self, mission_id: int) -> Dict[str, List[int]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT d.id, d.content
            FROM documents d
            JOIN mission_documents md ON md.document_id = d.id
            WHERE md.mission_id = ?
        """, (mission_id,))

        rows = cur.fetchall()
        conn.close()

        groups = {k: [] for k in CATEGORIES.keys()}
        groups["unknown"] = []

        for doc_id, content in rows:
            text = (content or "").lower()
            matched = False
            for cat, keywords in CATEGORIES.items():
                if any(kw in text for kw in keywords):
                    groups[cat].append(doc_id)
                    matched = True
            if not matched:
                groups["unknown"].append(doc_id)

        return groups
