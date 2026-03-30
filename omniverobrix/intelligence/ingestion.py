# omniverobrix/intelligence/ingestion.py

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(text: str) -> str:
    # Simple normalization for now; you can expand later
    return text.replace("\r\n", "\n").strip()


class IngestionEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------- PUBLIC ENTRY POINTS ----------

    def ingest_from_scanner_report(self, report_path: str, mission_id: Optional[int] = None) -> None:
        """
        Ingest documents from a JSON report produced by the scanner.
        Expected structure:
        {
          "files": [
            {
              "path": "...",
              "text": "...",
              "size_bytes": ...,
              "metadata": {...}
            },
            ...
          ]
        }
        """
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        files = data.get("files", [])
        for file_entry in files:
            self.ingest_single_file_entry(file_entry, mission_id=mission_id)

    def ingest_folder_raw(self, folder_path: str, mission_id: Optional[int] = None) -> None:
        """
        Fallback: walk a folder and ingest any text-like files directly.
        This bypasses the scanner and is optional.
        """
        for root, _, files in os.walk(folder_path):
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    # Skip non-text or unreadable files
                    continue

                file_entry = {
                    "path": full_path,
                    "text": text,
                    "size_bytes": os.path.getsize(full_path),
                    "metadata": {}
                }
                self.ingest_single_file_entry(file_entry, mission_id=mission_id)

    # ---------- CORE INGESTION LOGIC ----------

    def ingest_single_file_entry(self, file_entry: Dict[str, Any], mission_id: Optional[int] = None) -> int:
        """
        Ingest a single file entry from scanner or raw folder.
        Returns the document_id.
        """
        path = file_entry["path"]
        text = normalize_text(file_entry.get("text", "") or "")
        size_bytes = file_entry.get("size_bytes")
        metadata = file_entry.get("metadata", {}) or {}

        filename = os.path.basename(path)
        extension = os.path.splitext(filename)[1].lower() if "." in filename else ""

        file_hash = sha256_file(path)

        now = datetime.utcnow().isoformat()

        conn = self._connect()
        try:
            cur = conn.cursor()

            # Insert into documents
            cur.execute(
                """
                INSERT INTO documents (path, filename, extension, content, hash, size_bytes, created_at, updated_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    path,
                    filename,
                    extension,
                    text,
                    file_hash,
                    size_bytes,
                    now,
                    now,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            document_id = cur.lastrowid

            # Insert structured metadata
            self._insert_metadata(cur, document_id, metadata)

            # Link to mission if provided
            if mission_id is not None:
                cur.execute(
                    """
                    INSERT INTO mission_documents (mission_id, document_id)
                    VALUES (?, ?)
                    """,
                    (mission_id, document_id),
                )

            conn.commit()
            return document_id
        finally:
            conn.close()

    # ---------- HELPERS ----------

    def _insert_metadata(self, cur, document_id: int, metadata: Dict[str, Any]) -> None:
        """
        Flatten metadata dict into key/value rows.
        """
        for key, value in metadata.items():
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value)
            else:
                value_str = str(value)

            cur.execute(
                """
                INSERT INTO document_metadata (document_id, key, value)
                VALUES (?, ?, ?)
                """,
                (document_id, key, value_str),
            )


# ---------- SIMPLE CLI HOOK ----------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OmniVeroBrix Ingestion Engine")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scanner-report", help="Path to scanner JSON report")
    group.add_argument("--folder", help="Folder to ingest directly (raw text files)")
    parser.add_argument("--mission-id", type=int, help="Optional mission ID to link documents to")

    args = parser.parse_args()

    engine = IngestionEngine(db_path=args.db)

    if args.scanner_report:
        engine.ingest_from_scanner_report(args.scanner_report, mission_id=args.mission_id)
    elif args.folder:
        engine.ingest_folder_raw(args.folder, mission_id=args.mission_id)

    print("Ingestion complete.")
