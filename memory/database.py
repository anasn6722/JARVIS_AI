import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "memory.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        # ----------------------------
        # User Profile
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile(

            key TEXT PRIMARY KEY,
            value TEXT

        )
        """)

        # ----------------------------
        # Conversation History
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            speaker TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ----------------------------
        # Goals
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            completed INTEGER DEFAULT 0

        )
        """)

        # ----------------------------
        # Context Memory
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS context(

            key TEXT PRIMARY KEY,
            value TEXT

        )
        """)
        # ----------------------------
        # Notes
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ----------------------------
        # Events
        # ----------------------------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            event_date TEXT

        )
        """)
        self.conn.commit()


    # ======================================
    # Profile
    # ======================================

    def set_profile(self, key, value):

        self.cursor.execute(
            """
            INSERT INTO profile(key, value)
            VALUES(?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value=excluded.value
            """,
            (key, value),
        )

        self.conn.commit()


    def get_profile(self, key):

        self.cursor.execute(
            """
            SELECT value
            FROM profile
            WHERE key=?
            """,
            (key,),
        )

        row = self.cursor.fetchone()

        return row[0] if row else None

    # ==================================================
    # Context Memory
    # ==================================================

    def set_context(self, key, value):

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO context
            VALUES (?, ?)
            """,
            (key, str(value)),
        )

        self.conn.commit()

    def get_context(self, key):

        self.cursor.execute(
            """
            SELECT value
            FROM context
            WHERE key = ?
            """,
            (key,),
        )

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

    def add_history(self, speaker, message):

        self.cursor.execute(
            """
            INSERT INTO history(
                speaker,
                message
            )
            VALUES(?, ?)
            """,
            (
                speaker,
                message,
            ),
        )

        self.conn.commit()


    def get_history(self):

        self.cursor.execute(
            """
            SELECT
                speaker,
                message,
                timestamp
            FROM history
            ORDER BY id
            """
        )

        return self.cursor.fetchall()

    def delete_context(self, key):

        self.cursor.execute(
            """
            DELETE FROM context
            WHERE key = ?
            """,
            (key,),
        )

        self.conn.commit()


    # ==================================================
    # Notes
    # ==================================================   
    def add_note(self, note):
    
        self.cursor.execute(
            """
            INSERT INTO notes(note)
            VALUES(?)
            """,
            (note,),
        )  
        self.conn.commit() 
    def get_notes(self):
    
        self.cursor.execute(
            """
            SELECT note
            FROM notes
            ORDER BY id DESC
            """
        )  
        return [
            row[0]
            for row in self.cursor.fetchall()
        ]  
    # ==================================================
    # Events
    # ==================================================   
    def add_event(
        self,
        title,
        date,
    ): 
        self.cursor.execute(
            """
            INSERT INTO events(
                title,
                event_date
            )
            VALUES(?, ?)
            """,
            (
                title,
                date,
            ),
        )  
        self.conn.commit() 
    def get_events(self):
    
        self.cursor.execute(
            """
            SELECT
                title,
                event_date
            FROM events
            ORDER BY event_date
            """
        )  
        return self.cursor.fetchall()
    # ==================================================
    # Close Database
    # ==================================================

    def close(self):
            
        self.conn.close()