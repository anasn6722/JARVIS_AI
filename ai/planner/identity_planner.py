from ai.agent.task import Task
from ai.planner.planner import Planner


class IdentityPlanner(Planner):

    def can_plan(self, command):
        return command.intent == "identity"

    def plan(self, command):

        tasks = [
            Task(
                "identity",
                "",
            )
        ]

        print("=" * 50)
        print("IDENTITY PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks