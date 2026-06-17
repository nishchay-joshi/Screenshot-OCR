import sqlite3

from src.config import DB_PATH
DB_NAME = DB_PATH


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()

    conn.execute("""
                 CREATE TABLE IF NOT EXISTS screenshots
                 (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     path TEXT UNIQUE,
                     extracted_text TEXT,
                     screenshot_date TIMESTAMP
                 )
                 """)

    conn.commit()
    conn.close()


def screenshot_exists(path):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT 1
        FROM screenshots
        WHERE path = ?
        LIMIT 1
        """,
        (path,),
    ).fetchone()

    conn.close()

    return row is not None