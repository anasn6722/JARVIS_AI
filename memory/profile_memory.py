import json
from pathlib import Path


class ProfileMemory:
    FILE = Path("data/profile.json")

    def __init__(self):
        self.data = {}

        if self.FILE.exists():
            self.load()

    def load(self):
        with open(self.FILE, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def save(self):
        with open(self.FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                indent=4,
            )

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data.get(key)