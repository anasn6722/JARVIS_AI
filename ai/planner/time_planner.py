from ai.agent.task import Task
from ai.planner.planner import Planner


class TimePlanner(Planner):

    def can_plan(self, command):
        return command.intent == "time"

    def plan(self, command):

        tasks = [
            Task(
                "time",
                "",
            )
        ]

        print("=" * 50)
        print("TIME PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks