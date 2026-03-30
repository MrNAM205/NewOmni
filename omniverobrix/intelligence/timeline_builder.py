# omniverobrix/intelligence/timeline_builder.py

import re
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any


DATE_PATTERNS = [
    r"\b(\d{4}-\d{2}-\d{2})\b",                     # 2021-03-04
    r"\b(\d{2}/\d{2}/\d{4})\b",                     # 03/04/2021
    r"\b(\d{1,2} [A-Za-z]+ \d{4})\b",               # 4 March 2021
    r"\b([A-Za-z]+ \d{1,2}, \d{4})\b",              # March 4, 2021
]


def normalize_date(raw: str) -> Optional[str]:
    """
    Convert various date formats into ISO (YYYY-MM-DD).
    Returns None if parsing fails.
    """
    raw = raw.strip()

    # Try YYYY-MM-DD
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
    except:
        pass

    # Try MM/DD/YYYY
    try:
        return datetime.strptime(raw, "%m/%d/%Y").date().isoformat()
    except:
        pass

    # Try D Month YYYY
    try:
        return datetime.strptime(raw, "%d %B %Y").date().isoformat()
    except:
        pass

    # Try Month D, YYYY
    try:
        return datetime.strptime(raw, "%B %d, %Y").date().isoformat()
    except:
        pass

    return None


class TimelineBuilder:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def build_timeline_for_all_documents(self) -> int:
        """
        Extract timeline events for all documents.
        Returns number of events created.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, content FROM documents")
        rows = cur.fetchall()

        total_events = 0

        for doc_id, content in rows:
            events = self.extract_events_from_text(content)
            total_events += self._store_events(cur, doc_id, events)

        conn.commit()
        conn.close()
        return total_events

    def build_timeline_for_mission(self, mission_id: int) -> int:
        """
        Extract timeline events only for documents linked to a mission.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT d.id, d.content
            FROM documents d
            JOIN mission_documents md ON md.document_id = d.id
            WHERE md.mission_id = ?
        """, (mission_id,))

        rows = cur.fetchall()
        total_events = 0

        for doc_id, content in rows:
            events = self.extract_events_from_text(content)
            total_events += self._store_events(cur, doc_id, events)

        conn.commit()
        conn.close()
        return total_events

    # ---------------------------------------------------------
    # EVENT EXTRACTION
    # ---------------------------------------------------------

    def extract_events_from_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract (date, event_text) pairs from document text.
        """
        events = []

        for pattern in DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                raw_date = match.group(1)
                iso_date = normalize_date(raw_date)
                if not iso_date:
                    continue

                # Extract surrounding context (sentence)
                event_text = self._extract_sentence(text, match.start())

                events.append((iso_date, event_text))

        return events

    def _extract_sentence(self, text: str, index: int) -> str:
        """
        Extract the sentence around a given index.
        """
        start = text.rfind(".", 0, index)
        end = text.find(".", index)

        if start == -1:
            start = 0
        else:
            start += 1

        if end == -1:
            end = len(text)

        return text[start:end].strip()

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------

    def _store_events(self, cur, document_id: int, events: List[Tuple[str, str]]) -> int:
        """
        Store extracted events in the timeline_events table.
        """
        count = 0
        for date, text in events:
            cur.execute(
                """
                INSERT INTO timeline_events (document_id, event_date, event_text, confidence)
                VALUES (?, ?, ?, ?)
                """,
                (document_id, date, text, 1.0),
            )
            count += 1
        return count


# ---------------------------------------------------------
# OPTIONAL CLI ENTRYPOINT
# ---------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OmniVeroBrix Timeline Builder")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--mission-id", type=int, help="Build timeline only for a mission")

    args = parser.parse_args()

    builder = TimelineBuilder(db_path=args.db)

    if args.mission_id:
        count = builder.build_timeline_for_mission(args.mission_id)
        print(f"Extracted {count} events for mission {args.mission_id}.")
    else:
        count = builder.build_timeline_for_all_documents()
        print(f"Extracted {count} events from all documents.")
