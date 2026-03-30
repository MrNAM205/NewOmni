import sqlite3

def init_db():
    """
    Initializes the database and creates the tables.
    """
    conn = sqlite3.connect('omniverobrix.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        filename TEXT NOT NULL,
        extension TEXT,
        content TEXT,
        hash TEXT,
        size_bytes INTEGER,
        created_at TEXT,
        updated_at TEXT,
        metadata_json TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        vector BLOB NOT NULL,
        model TEXT NOT NULL,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        event_date TEXT NOT NULL,
        event_text TEXT NOT NULL,
        confidence REAL DEFAULT 1.0,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        entity TEXT NOT NULL,
        entity_type TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS definitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        source TEXT NOT NULL,
        definition TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mission_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_id INTEGER NOT NULL,
        document_id INTEGER NOT NULL,
        FOREIGN KEY (mission_id) REFERENCES missions(id),
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tool_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_name TEXT NOT NULL,
        input_json TEXT,
        output_json TEXT,
        timestamp TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS context_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        value TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        value TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duplicates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash TEXT NOT NULL,
        document_id INTEGER NOT NULL,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS folder_signatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_path TEXT NOT NULL,
        signature_hash TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
