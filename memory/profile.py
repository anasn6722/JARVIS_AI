from memory.database import Database


class ProfileMemory:

    def __init__(self):

        self.db = Database()

    def set(self, key, value):

        self.db.cursor.execute(

            """
            INSERT OR REPLACE INTO profile
            VALUES(?,?)
            """,

            (key, value)

        )

        self.db.conn.commit()

    def get(self, key):

        self.db.cursor.execute(

            """
            SELECT value
            FROM profile
            WHERE key=?
            """,

            (key,)

        )

        row = self.db.cursor.fetchone()

        if row:
            return row[0]

        return None