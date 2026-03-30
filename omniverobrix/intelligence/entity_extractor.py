# omniverobrix/intelligence/entity_extractor.py

import re
import sqlite3
from typing import List, Tuple, Optional, Dict, Any


# ---------------------------------------------------------
# BASIC REGEX PATTERNS (Phase 1)
# ---------------------------------------------------------

PERSON_PATTERN = r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b"   # John Smith
ORG_PATTERN = r"\b([A-Z][A-Za-z]+ (County|Court|Agency|Department|Office))\b"
LEGAL_TERM_PATTERN = r"\b(deed|notice|tax|assessment|probate|hearing|affidavit|trust|title)\b"
LOCATION_PATTERN = r"\b([A-Z][a-z]+,? [A-Z]{2})\b"  # Birmingham, AL


class EntityExtractor:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def extract_entities_for_all_documents(self) -> int:
        """
        Extract entities for every document in the DB.
        Returns number of entities created.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id, content FROM documents")
        rows = cur.fetchall()

        total = 0
        for doc_id, content in rows:
            entities = self.extract_entities_from_text(content)
            total += self._store_entities(cur, doc_id, entities)

        conn.commit()
        conn.close()
        return total

    def extract_entities_for_mission(self, mission_id: int) -> int:
        """
        Extract entities only for documents linked to a mission.
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
        total = 0

        for doc_id, content in rows:
            entities = self.extract_entities_from_text(content)
            total += self._store_entities(cur, doc_id, entities)

        conn.commit()
        conn.close()
        return total

    # ---------------------------------------------------------
    # ENTITY EXTRACTION
    # ---------------------------------------------------------

    def extract_entities_from_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Returns list of (entity, entity_type)
        """
        entities = []

        # People
        for match in re.findall(PERSON_PATTERN, text):
            entities.append((match, "person"))

        # Organizations
        for match in re.findall(ORG_PATTERN, text):
            entities.append((match[0], "organization"))

        # Legal terms
        for match in re.findall(LEGAL_TERM_PATTERN, text, flags=re.IGNORECASE):
            entities.append((match.lower(), "legal_term"))

        # Locations
        for match in re.findall(LOCATION_PATTERN, text):
            entities.append((match, "location"))

        return entities

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------

    def _store_entities(self, cur, document_id: int, entities: List[Tuple[str, str]]) -> int:
        """
        Store extracted entities in the DB.
        """
        count = 0
        for entity, entity_type in entities:
            cur.execute(
                """
                INSERT INTO entities (document_id, entity, entity_type)
                VALUES (?, ?, ?)
                """,
                (document_id, entity, entity_type),
            )
            count += 1
        return count

    # ---------------------------------------------------------
    # DEFINITION LOOKUP
    # ---------------------------------------------------------

    def lookup_definitions(self, terms: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """
        Look up definitions for a list of terms.
        Returns:
        {
            "deed": [
                {"source": "Black's", "definition": "..."},
                {"source": "Bouvier's", "definition": "..."}
            ],
            ...
        }
        """
        conn = self._connect()
        cur = conn.cursor()

        results = {}

        for term in terms:
            cur.execute("""
                SELECT source, definition
                FROM definitions
                WHERE LOWER(term) = LOWER(?)
            """, (term,))

            rows = cur.fetchall()
            results[term] = [{"source": src, "definition": d} for src, d in rows]

        conn.close()
        return results


# ---------------------------------------------------------
# OPTIONAL CLI ENTRYPOINT
# ---------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OmniVeroBrix Entity Extractor")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--mission-id", type=int, help="Extract entities only for a mission")

    args = parser.parse_args()

    extractor = EntityExtractor(db_path=args.db)

    if args.mission_id:
        count = extractor.extract_entities_for_mission(args.mission_id)
        print(f"Extracted {count} entities for mission {args.mission_id}.")
    else:
        count = extractor.extract_entities_for_all_documents()
        print(f"Extracted {count} entities from all documents.")
