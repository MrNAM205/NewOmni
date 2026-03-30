# omniverobrix/intelligence/semantic_indexer.py

import sqlite3
import numpy as np
import json
from typing import List, Tuple, Optional, Any, Dict
from datetime import datetime


class SemanticIndexer:
    def __init__(self, db_path: str, embed_fn):
        """
        embed_fn: a function that takes text -> numpy vector
        Example:
            embed_fn("hello world") -> np.array([...], dtype=float32)
        """
        self.db_path = db_path
        self.embed_fn = embed_fn

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def index_all_unembedded_documents(self) -> int:
        """
        Find all documents that do NOT have embeddings yet,
        generate embeddings, and store them.
        Returns number of documents embedded.
        """
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT d.id, d.content
            FROM documents d
            LEFT JOIN embeddings e ON d.id = e.document_id
            WHERE e.id IS NULL
        """)

        rows = cur.fetchall()
        count = 0

        for doc_id, content in rows:
            if not content:
                continue

            vector = self.embed_fn(content)
            self._store_embedding(cur, doc_id, vector)
            count += 1

        conn.commit()
        conn.close()
        return count

    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Semantic search.
        Returns list of (document_id, score) sorted by score descending.
        """
        query_vec = self.embed_fn(query)
        query_vec = query_vec.astype(np.float32)

        conn = self._connect()
        cur = conn.cursor()

        cur.execute("SELECT document_id, vector FROM embeddings")
        rows = cur.fetchall()

        scores = []
        for doc_id, blob in rows:
            vec = np.frombuffer(blob, dtype=np.float32)
            score = self._cosine_similarity(query_vec, vec)
            scores.append((doc_id, score))

        conn.close()

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _store_embedding(self, cur, document_id: int, vector: np.ndarray) -> None:
        """
        Store embedding vector in SQLite as BLOB.
        """
        now = datetime.utcnow().isoformat()
        blob = vector.astype(np.float32).tobytes()

        cur.execute(
            """
            INSERT INTO embeddings (document_id, vector, model)
            VALUES (?, ?, ?)
            """,
            (document_id, blob, "omniverobrix-local-embed-v1"),
        )

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.
        """
        denom = (np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)


# ---------------------------------------------------------
# OPTIONAL CLI ENTRYPOINT
# ---------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import numpy as np

    # Dummy embedding function for testing
    def dummy_embed(text: str) -> np.ndarray:
        return np.random.rand(384).astype(np.float32)

    parser = argparse.ArgumentParser(description="OmniVeroBrix Semantic Indexer")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--index", action="store_true", help="Index all unembedded documents")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args()

    indexer = SemanticIndexer(db_path=args.db, embed_fn=dummy_embed)

    if args.index:
        count = indexer.index_all_unembedded_documents()
        print(f"Indexed {count} documents.")

    if args.search:
        results = indexer.search(args.search, top_k=args.top_k)
        print("Search results:")
        for doc_id, score in results:
            print(f"  Document {doc_id} — score {score:.4f}")
