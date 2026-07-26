class ChatMemory:
    def __init__(self):
        self.history = []

    def add(self, speaker: str, message: str):
        self.history.append(
            {
                "speaker": speaker,
                "message": message,
            }
        )

    def last(self):
        if self.history:
            return self.history[-1]

        return None

    def clear(self):
        self.history.clear()

    def get_all(self):
        return self.history