import sqlite3
from datetime import datetime

def ingest_document(db_path: str, path: str, content: str, hash_value: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (path, filename, extension, content, hash, size_bytes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        path,
        path.replace("/", "\\").split("\\")[-1],
        path.split(".")[-1] if "." in path else "",
        content,
        hash_value,
        len(content.encode("utf-8")),
        datetime.utcnow().isoformat()
    ))

    doc_id = cur.lastrowid
    conn.commit()
    conn.close()
    return doc_id