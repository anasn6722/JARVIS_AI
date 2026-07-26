import json
from pathlib import Path


class ChatMemory:
    def __init__(self):
        self.file = Path("data/history.json")
        self.history = []

        self.load()

    def add(self, speaker: str, message: str):
        self.history.append(
            {
                "speaker": speaker,
                "message": message,
            }
        )

        self.save()

    def last(self):
        if self.history:
            return self.history[-1]

        return None

    def clear(self):
        self.history.clear()
        self.save()

    def get_all(self):
        return self.history

    def load(self):
        if self.file.exists():

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                self.history = json.load(f)

    def save(self):
        with open(
            self.file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.history,
                f,
                indent=4,
            )