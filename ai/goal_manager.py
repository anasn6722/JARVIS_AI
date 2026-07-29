import json
from pathlib import Path


class GoalManager:

    FILE = Path("data/goals.json")

    def __init__(self):
        self.FILE.parent.mkdir(exist_ok=True)

        if not self.FILE.exists():
            self.FILE.write_text(
                "[]",
                encoding="utf-8",
            )

        self.goals = self.load()

    def load(self):
        with open(
            self.FILE,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def save(self):
        with open(
            self.FILE,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                self.goals,
                f,
                indent=4,
            )

    def add(self, goal):
        goal = goal.strip()

        if goal and goal not in self.goals:
            self.goals.append(goal)
            self.save()

    def remove(self, goal):
        if goal in self.goals:
            self.goals.remove(goal)
            self.save()

    def all(self):
        return self.goals

    def clear(self):
        self.goals = []
        self.save()