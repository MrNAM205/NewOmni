# omniverobrix/missions/manager/manager.py

import sqlite3
from typing import List, Dict, Any, Optional


class MissionManager:
    """
    Phase 4 Mission Manager:
    - Create missions
    - List missions
    - Activate missions
    - Attach documents
    - Query mission metadata
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    # ---------------------------------------------------------
    # DB Helpers
    # ---------------------------------------------------------

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # Mission Creation
    # ---------------------------------------------------------

    def create(self, mission_type: str, description: str = "") -> int:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO missions (name, description)
            VALUES (?, ?)
            """,
            (mission_type, description),
        )

        mission_id = cur.lastrowid
        conn.commit()
        conn.close()

        return mission_id

    # ---------------------------------------------------------
    # Mission Listing
    # ---------------------------------------------------------

    def list(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, description, created_at
            FROM missions
            ORDER BY id ASC
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]

    # ---------------------------------------------------------
    # Mission Activation
    # ---------------------------------------------------------

    def activate(self, mission_id: int, context_manager) -> bool:
        """
        Stores active mission in context_state.
        """
        if not self.exists(mission_id):
            return False

        context_manager.set("active_mission_id", str(mission_id))
        return True

    def get_active(self, context_manager) -> Optional[int]:
        val = context_manager.get("active_mission_id")
        if val is None:
            return None
        try:
            return int(val)
        except ValueError:
            return None

    # ---------------------------------------------------------
    # Mission Metadata
    # ---------------------------------------------------------

    def info(self, mission_id: int) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, description, created_at
            FROM missions
            WHERE id = ?
        """, (mission_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3],
        }

    # ---------------------------------------------------------
    # Document Attachment
    # ---------------------------------------------------------

    def attach_documents(self, mission_id: int, document_ids: List[int]) -> int:
        if not self.exists(mission_id):
            return 0

        conn = self._connect()
        cur = conn.cursor()

        count = 0
        for doc_id in document_ids:
            cur.execute(
                """
                INSERT INTO mission_documents (mission_id, document_id)
                VALUES (?, ?)
                """,
                (mission_id, doc_id),
            )
            count += 1

        conn.commit()
        conn.close()
        return count

    # ---------------------------------------------------------
    # Existence Check
    # ---------------------------------------------------------

    def exists(self, mission_id: int) -> bool:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM missions WHERE id = ?", (mission_id,))
        row = cur.fetchone()

        conn.close()
        return row is not None
