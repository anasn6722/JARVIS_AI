from memory.database import Database


class ProfileMemory:

    def __init__(self, db):

        self.db = db    


    def set(self,key,value):

        self.db.cursor.execute(
            """
            INSERT INTO profile(key,value)
            VALUES(?,?)
            ON CONFLICT(key)
            DO UPDATE SET value=excluded.value
            """,
            (
                key,
                value,
            )
        )

        self.db.conn.commit()



    def get(self,key):

        self.db.cursor.execute(
            """
            SELECT value
            FROM profile
            WHERE key=?
            """,
            (key,)
        )

        row=self.db.cursor.fetchone()

        if row:
            return row[0]

        return None