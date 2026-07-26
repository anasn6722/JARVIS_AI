import json
from pathlib import Path


class ProfileMemory:
    def __init__(self):
        self.file = Path("data/profile.json")
        self.profile = {}

        self.load()

    def load(self):
        if self.file.exists():
            try:
                with self.file.open(
                    "r",
                    encoding="utf-8",
                ) as file:
                    self.profile = json.load(file)

            except json.JSONDecodeError:
                self.profile = {}

    def save(self):
        with self.file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.profile,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def set(self, key, value):
        self.profile[key] = value
        self.save()

    def get(self, key):
        return self.profile.get(key)