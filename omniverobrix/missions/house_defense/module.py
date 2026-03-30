# omniverobrix/missions/house_defense/module.py

import sqlite3
from typing import Dict, Any, List

from omniverobrix.missions.house_defense.document_classifier import HouseDocumentClassifier
from omniverobrix.missions.house_defense.summarizer import HouseDefenseSummarizer
from omniverobrix.missions.house_defense.question_generator import HouseDefenseQuestionGenerator


class HouseDefenseModule:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.classifier = HouseDocumentClassifier(db_path)
        self.summarizer = HouseDefenseSummarizer(db_path)
        self.qgen = HouseDefenseQuestionGenerator()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def run(self, mission_id: int) -> Dict[str, Any]:
        """
        Main entry point for the House Defense mission.
        """
        document_groups = self.classifier.classify_mission_documents(mission_id)
        timeline_events = self._load_timeline_events_for_mission(mission_id)
        entities = self._load_entities_for_mission(mission_id)

        summary = self.summarizer.build_summary(
            mission_id=mission_id,
            document_groups=document_groups,
            timeline_events=timeline_events,
            entities=entities,
        )

        questions = self.qgen.generate_questions(summary, document_groups)

        return {
            "mission": "house_defense",
            "mission_id": mission_id,
            "document_groups": document_groups,
            "timeline": timeline_events,
            "entities": entities,
            "summary": summary,
            "questions": questions,
        }

    def _load_timeline_events_for_mission(self, mission_id: int) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT te.id, te.document_id, te.event_date, te.event_text
            FROM timeline_events te
            JOIN mission_documents md ON md.document_id = te.document_id
            WHERE md.mission_id = ?
            ORDER BY te.event_date ASC
        """, (mission_id,))

        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "event_date": row[2],
                "event_text": row[3],
            }
            for row in rows
        ]

    def _load_entities_for_mission(self, mission_id: int) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT e.id, e.document_id, e.entity, e.entity_type
            FROM entities e
            JOIN mission_documents md ON md.document_id = e.document_id
            WHERE md.mission_id = ?
        """, (mission_id,))

        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "entity": row[2],
                "entity_type": row[3],
            }
            for row in rows
        ]
