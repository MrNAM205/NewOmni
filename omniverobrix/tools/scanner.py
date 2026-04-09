import os
import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

from omniverobrix.ingestion.extract_text import extract_text_from_file
from omniverobrix.ingestion.ocr import try_ocr
from omniverobrix.ingestion.pipeline import ingest_document


class FolderScanner:
    """
    NOW MODE Scanner:
    - Dynamic folder scanning
    - File hashing
    - Duplicate detection
    - OCR (Tesseract -> PaddleOCR fallback)
    - Full ingestion pipeline
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _hash_file(self, path: str) -> str:
        sha = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                while chunk := f.read(8192):
                    sha.update(chunk)
            return sha.hexdigest()
        except Exception:
            return None

    def _record_folder_signature(self, folder: str, signature: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO folder_signatures (folder_path, signature_hash)
            VALUES (?, ?)
        """, (folder, signature))
        conn.commit()
        conn.close()

    def _record_duplicate(self, hash_value: str, document_id: int):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO duplicates (hash, document_id)
            VALUES (?, ?)
        """, (hash_value, document_id))
        conn.commit()
        conn.close()

    def scan_folders(self, folders: List[str]) -> Dict[str, Any]:
        report = {
            "type": "scan_report",
            "folders_scanned": [],
            "files_found": [],
            "ingested": [],
            "duplicates": [],
            "errors": []
        }

        for folder in folders:
            if not os.path.exists(folder):
                report["errors"].append(f"Folder not found: {folder}")
                continue

            report["folders_scanned"].append(folder)
            folder_hash_accumulator = hashlib.sha256()

            for root, _, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    report["files_found"].append(full_path)
                    file_hash = self._hash_file(full_path)
                    if file_hash:
                        folder_hash_accumulator.update(file_hash.encode())
                    try:
                        text = extract_text_from_file(full_path)
                        if not text:
                            text = try_ocr(full_path)
                        if text:
                            doc_id = ingest_document(
                                db_path=self.db_path,
                                path=full_path,
                                content=text,
                                hash_value=file_hash
                            )
                            report["ingested"].append(full_path)
                        else:
                            report["errors"].append(f"No text extracted: {full_path}")
                    except Exception as e:
                        report["errors"].append(f"Error processing {full_path}: {e}")
            folder_signature = folder_hash_accumulator.hexdigest()
            self._record_folder_signature(folder, folder_signature)
        return report