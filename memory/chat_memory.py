from memory.database import Database


class ChatMemory:

    def __init__(self, db: Database):
        self.db = db

    def add(self, speaker: str, message: str):
        self.db.add_history(speaker, message)

    def recent(self, limit=10):
        history = self.db.get_history()
        return history[-limit:]

    def last(self):
        history = self.db.get_history()
        if history:
            speaker, message, timestamp = history[-1]
            return {
                "speaker": speaker,
                "message": message,
                "timestamp": timestamp,
            }
        return None

    def clear(self):
        self.db.cursor.execute("DELETE FROM history")
        self.db.conn.commit()

    def get_all(self):
        return self.db.get_history()