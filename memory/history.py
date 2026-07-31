from memory.database import Database


class HistoryMemory:

    def __init__(self):

        self.db = Database()

    def add(self, speaker, message):

        self.db.cursor.execute(

            """
            INSERT INTO history(
                speaker,
                message
            )

            VALUES(?,?)
            """,

            (speaker, message)

        )

        self.db.conn.commit()

    def last(self, limit=10):

        self.db.cursor.execute(

            """
            SELECT speaker,message

            FROM history

            ORDER BY id DESC

            LIMIT ?
            """,

            (limit,)

        )

        return self.db.cursor.fetchall()