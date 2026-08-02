import json
from datetime import datetime
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
        try:
            with open(
                self.FILE,
                "r",
                encoding="utf-8",
            ) as f:
                goals = json.load(f)
    
        except (FileNotFoundError, json.JSONDecodeError):
            goals = []
            with open(
                self.FILE,
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(goals, f, indent=4)
    
        migrated = []
    
        for goal in goals:
        
            if isinstance(goal, str):
                migrated.append(
                    {
                        "title": goal,
                        "created": "",
                        "deadline": "",
                        "progress": 0,
                        "completed": False,
                        "tasks": [],
                    }
                )
            else:
                migrated.append(goal)
    
        self.goals = migrated
        self.save()
    
        return migrated
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

    def add(
        self,
        title,
        deadline="",
    ):

        title = title.strip()

        if not title:
            return

        goal = {
            "title": title,
            "created": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "deadline": deadline,
            "progress": 0,
            "completed": False,
            "tasks": [],
        }

        self.goals.append(goal)

        self.save()

    def remove(self, title):

        self.goals = [
            goal
            for goal in self.goals
            if goal["title"] != title
        ]

        self.save()

    def all(self):

        return self.goals

    def clear(self):

        self.goals = []

        self.save()

    def update_progress(
        self,
        title,
        progress,
    ):

        for goal in self.goals:

            if goal["title"] == title:

                goal["progress"] = max(
                    0,
                    min(progress, 100),
                )

                if goal["progress"] == 100:
                    goal["completed"] = True

                break

        self.save()

    def add_task(
        self,
        title,
        task,
    ):

        for goal in self.goals:

            if goal["title"] == title:

                goal["tasks"].append(
                    {
                        "task": task,
                        "done": False,
                    }
                )

                break

        self.save()

    def complete_task(
        self,
        title,
        task,
    ):

        for goal in self.goals:

            if goal["title"] == title:

                for t in goal["tasks"]:

                    if t["task"] == task:

                        t["done"] = True

                total = len(goal["tasks"])

                if total:

                    done = sum(
                        1
                        for t in goal["tasks"]
                        if t["done"]
                    )

                    goal["progress"] = int(
                        done / total * 100
                    )

                    if all(t["done"] for t in goal["tasks"]):
                    
                        goal["completed"] = True
                        goal["progress"] = 100

                break

        self.save()

    def next_task(self, title):

        for goal in self.goals:

            if goal["title"] == title:

                for task in goal["tasks"]:

                    if not task["done"]:
                        return task

        return None

    def progress(self, title):

        for goal in self.goals:

            if goal["title"] == title:

                total = len(goal["tasks"])

                if total == 0:
                    return 0

                done = sum(
                    1
                    for task in goal["tasks"]
                    if task["done"]
                )

                return int(done / total * 100)

        return 0

    def complete_goal(self, title):

        for goal in self.goals:

            if goal["title"] == title:

                goal["completed"] = True
                goal["progress"] = 100

                for task in goal["tasks"]:
                    task["done"] = True

                self.save()

                return True

        return False