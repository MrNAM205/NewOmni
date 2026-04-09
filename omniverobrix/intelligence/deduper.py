import hashlib
import sqlite3
import math
from datetime import datetime
from typing import Optional, List, Tuple

class Deduper:
    """
    Handles multi-stage deduplication:
    1. Exact File Hash (SHA-256)
    2. Exact Content Hash (SHA-256 of text)
    3. Semantic Similarity (Cosine similarity of embeddings)
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def calculate_file_hash(self, file_path: str) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def calculate_content_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        if not magnitude1 or not magnitude2:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def check_file_exists(self, file_hash: str) -> Optional[int]:
        """Returns document_id if exact file hash exists."""
        with self._get_conn() as conn:
            res = conn.execute("SELECT document_id FROM file_hash_index WHERE file_hash = ?", (file_hash,)).fetchone()
            return res[0] if res else None

    def check_content_exists(self, content_hash: str) -> Optional[int]:
        """Returns document_id if exact content hash exists."""
        with self._get_conn() as conn:
            res = conn.execute("SELECT document_id FROM content_hash_index WHERE content_hash = ?", (content_hash,)).fetchone()
            return res[0] if res else None

    def find_semantic_duplicates(self, embedding: List[float], threshold: float = 0.95) -> List[Tuple[int, float]]:
        """
        Compares current embedding against all stored embeddings in the database.
        Returns list of (document_id, similarity_score).
        """
        duplicates = []
        with self._get_conn() as conn:
            # Assuming embeddings are stored in 'documents' table or a linked vector table
            # Here we pull id and embedding to compare
            cursor = conn.execute("SELECT id, embedding_json FROM documents WHERE embedding_json IS NOT NULL")
            for doc_id, emb_json in cursor:
                stored_emb = list(map(float, emb_json.split(','))) # Example storage format
                score = self.cosine_similarity(embedding, stored_emb)
                if score >= threshold:
                    duplicates.append((doc_id, score))
        return duplicates

    def register_file_hash(self, file_hash: str, file_path: str, document_id: int):
        now = datetime.utcnow().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO file_hash_index (file_hash, file_path, document_id, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?)
            """, (file_hash, file_path, document_id, now, now))
            conn.commit()

    def register_content_hash(self, content_hash: str, document_id: int):
        now = datetime.utcnow().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO content_hash_index (content_hash, document_id, first_seen, last_seen)
                VALUES (?, ?, ?, ?)
            """, (content_hash, document_id, now, now))
            conn.commit()

    def register_semantic_duplicate(self, source_id: int, duplicate_id: int, similarity: float, method: str = "cosine"):
        now = datetime.utcnow().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO semantic_duplicates (source_document_id, duplicate_document_id, similarity, method, detected_at)
                VALUES (?, ?, ?, ?, ?)
            """, (source_id, duplicate_id, similarity, method, now))
            conn.commit()

    def process_document(self, path: str, text: str, embedding: Optional[List[float]] = None):
        """
        High-level orchestration for a new document candidate.
        """
        f_hash = self.calculate_file_hash(path)
        if doc_id := self.check_file_exists(f_hash):
            return {"status": "duplicate", "type": "file", "id": doc_id}

        c_hash = self.calculate_content_hash(text)
        if doc_id := self.check_content_exists(c_hash):
            return {"status": "duplicate", "type": "content", "id": doc_id}

        if embedding:
            sem_dupes = self.find_semantic_duplicates(embedding)
            if sem_dupes:
                # Return the best match
                best_match = max(sem_dupes, key=lambda x: x[1])
                return {"status": "near-duplicate", "type": "semantic", "id": best_match[0], "score": best_match[1]}

        return {"status": "unique", "file_hash": f_hash, "content_hash": c_hash}