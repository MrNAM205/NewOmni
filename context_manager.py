import sqlite3
from typing import Optional

class ContextManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def set(self, key: str, value: str):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO context_state (key, value) VALUES (?, ?)", (key, str(value)))
            conn.commit()
        finally:
            conn.close()

    def get(self, key: str) -> Optional[str]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT value FROM context_state WHERE key = ? ORDER BY id DESC LIMIT 1", (key,))
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            conn.close()