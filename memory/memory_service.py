from memory.database import Database


class MemoryService:

    def __init__(self):
        self.db = Database()

    # ----------------------------
    # Profile Memory
    # ----------------------------

    def remember(self, key, value):
        self.db.set_profile(key, value)

    def recall(self, key):
        return self.db.get_profile(key)

    # ----------------------------
    # Notes
    # ----------------------------

    def save_note(self, note):
        self.db.add_note(note)

    def notes(self):
        return self.db.get_notes()

    # ----------------------------
    # Conversation History
    # ----------------------------

    def save_chat(self, speaker, message):
        self.db.add_history(
            speaker,
            message,
        )

    def history(self):
        return self.db.get_history()

    # ----------------------------
    # Events
    # ----------------------------

    def remember_event(
        self,
        title,
        date,
    ):
        self.db.add_event(
            title,
            date,
        )

    def upcoming_events(self):
        return self.db.get_events()