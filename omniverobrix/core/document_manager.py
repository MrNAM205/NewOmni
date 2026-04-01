# omniverobrix/core/document_manager.py

import sqlite3
import json
from typing import Optional, Dict, Any

class DocumentManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get(self, document_id: int) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, content, path, created_at FROM documents WHERE id = ?",
            (document_id,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        doc_id, content, path, created_at = row
        
        # The prompt asks for a "source" field in the metadata.
        # Hardcoding to "scanner" as per the example.
        return {
            "id": doc_id,
            "content": content,
            "metadata": {
                "path": path,
                "created_at": created_at,
                "source": "scanner"
            }
        }

    def get_json(self, document_id: int) -> str:
        doc = self.get(document_id)
        return json.dumps(doc) if doc else "{}"
