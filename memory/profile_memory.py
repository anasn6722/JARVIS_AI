from memory.database import Database


class ProfileMemory:

    def __init__(self, db: Database):
        self.db = db

    def set(self, key, value):
        self.db.set_profile(key, value)

    def get(self, key):
        return self.db.get_profile(key)