import sqlite3

def initialize_db(db_path="omniverobrix.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    schema = [
        """CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, filename TEXT, extension TEXT, 
            content TEXT, hash TEXT, size_bytes INTEGER, created_at TEXT, updated_at TEXT, metadata_json TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS document_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, key TEXT, value TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, vector BLOB, model TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, event_date TEXT, event_text TEXT, confidence REAL,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, entity TEXT, entity_type TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT, source TEXT, definition TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, created_at TEXT, updated_at TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS mission_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, mission_id INTEGER, document_id INTEGER,
            FOREIGN KEY (mission_id) REFERENCES missions(id), FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS tool_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tool_name TEXT, input_json TEXT, output_json TEXT, timestamp TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS context_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS system_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS duplicates (
            id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, document_id INTEGER,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )""",
        """CREATE TABLE IF NOT EXISTS folder_signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT, folder_path TEXT, signature_hash TEXT
        )"""
    ]
    
    for query in schema:
        cur.execute(query)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    initialize_db()