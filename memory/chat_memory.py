from memory.database import Database


class ChatMemory:

    def __init__(self, db: Database):
        self.db = db


    def add(
        self,
        speaker: str,
        message: str,
    ):
        self.db.add_history(
            speaker,
            message,
        )


    def _convert_rows(self, rows):

        return [
            {
                "speaker": row[0],
                "message": row[1],
                "timestamp": row[2],
            }
            for row in rows
        ]


    def recent(self, limit=10):

        history = self.db.get_history()

        history = self._convert_rows(history)

        return history[-limit:]


    def last(self):

        history = self.db.get_history()

        history = self._convert_rows(history)

        if history:
            return history[-1]

        return None


    def clear(self):

        self.db.cursor.execute(
            "DELETE FROM history"
        )

        self.db.conn.commit()


    def get_all(self):

        history = self.db.get_history()

        return self._convert_rows(history)