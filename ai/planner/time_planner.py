from ai.agent.task import Task
from ai.planner.planner import Planner


class TimePlanner(Planner):
    """Plans time-related commands."""

    def can_plan(self, command):
        return command.intent == "time"

    def plan(self, command):
        tasks = [
            Task(
                action="time",
                target="",
            )
        ]

        # -------------------------
        # DEBUG
        # -------------------------

        print("=" * 50)
        print("TIME PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks