from ai.agent.task import Task
from ai.planner.planner import Planner


class GoalPlanner(Planner):

    def __init__(
        self,
        goal_ai_planner,
        task_parser,
    ):
        self.goal_ai_planner = goal_ai_planner
        self.task_parser = task_parser

    def can_plan(self, command):

        return command.intent in (
            "add_goal",
            "show_goals",
            "next_task",
            "complete_task",
            "goal_progress",
            "delete_goal",
        )

    def plan(self, command):

        # -------------------------
        # Rule-based goal commands
        # -------------------------

        if command.intent != "add_goal":

            tasks = [

                Task(

                    action=command.intent,

                    target=command.original,

                )

            ]

        # -------------------------
        # AI Goal Decomposition
        # -------------------------

        else:

            ai_tasks = self.goal_ai_planner.create_plan(
                command.original
            )

            tasks = self.task_parser.parse(
                ai_tasks
            )

        print("=" * 50)
        print("GOAL PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks