from ai.agent.task import Task
from ai.planner.planner import Planner


class MemoryPlanner(Planner):

    def can_plan(self, command):

        return command.intent in (
            "set_name",
            "get_name",
            "set_preference",
            "get_preference",
            "history",
            "last_message",
        )

    def plan(self, command):

        tasks = []

        tasks.append(
            Task(
                command.intent,
                command.original,
            )
        )

        print("=" * 50)
        print("MEMORY PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks