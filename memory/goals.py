from memory.database import Database


class GoalMemory:

    def __init__(self, db):

        self.db = db

    def add(self, goal):

        self.db.cursor.execute(

            """
            INSERT INTO goals(goal)
            VALUES(?)
            """,

            (goal,)

        )

        self.db.conn.commit()

    def all(self):

        self.db.cursor.execute(

            """
            SELECT goal,completed

            FROM goals
            """
        )

        return self.db.cursor.fetchall()