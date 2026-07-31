from memory.database import Database


class ProfileMemory:

    def __init__(self):

        self.db = Database()

    def set(self, key, value):
        print("Saving:", key, value)

        self.db.cursor.execute(

            """
            INSERT OR REPLACE INTO profile
            VALUES(?,?)
            """,

            (key, value)

        )

        self.db.conn.commit()

    def get(self, key):
        print("Looking for:", key)

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

    # NEW
    def all(self):
        self.db.cursor.execute(
            """
            SELECT key, value
            FROM profile
            """
        )

        return self.db.cursor.fetchall()

    # NEW
    def delete(self, key):
        self.db.cursor.execute(
            """
            DELETE FROM profile
            WHERE key = ?
            """,
            (key,),
        )

        self.db.conn.commit()