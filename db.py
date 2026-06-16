import sqlite3

DB_NAME = "db.sqlite"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS screenshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        extracted_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()