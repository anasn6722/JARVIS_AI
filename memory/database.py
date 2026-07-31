import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "memory.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile(

            key TEXT PRIMARY KEY,
            value TEXT

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            speaker TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            completed INTEGER DEFAULT 0

        )
        """)

        self.conn.commit()