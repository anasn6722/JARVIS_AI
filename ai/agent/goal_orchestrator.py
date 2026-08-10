from ai.agent.goal_decomposer import GoalDecomposer
from ai.agent.goal_executor import GoalExecutor


class GoalOrchestrator:
    """Coordinate goal planning and execution."""

    def __init__(
        self,
        goal_decomposer: GoalDecomposer,
        goal_executor: GoalExecutor,
    ):
        self.goal_decomposer = goal_decomposer
        self.goal_executor = goal_executor

    def execute(self, goal_text):
        """Decompose and execute a natural-language goal."""

        if not goal_text:
            return False, "No goal provided."

        goal_text = goal_text.strip()

        if not goal_text:
            return False, "No goal provided."

        print("=" * 60)
        print("GOAL ORCHESTRATOR")
        print("=" * 60)

        print("Goal:", goal_text)

        try:
            print("\n=== DECOMPOSING GOAL ===")

            goal_plan = self.goal_decomposer.decompose(
                goal_text,
            )

            if not goal_plan:
                return False, "Could not create a goal plan."

            print(
                "Goal:",
                goal_plan.goal.title,
            )

            print(
                "Tasks:",
                len(goal_plan.goal.tasks),
            )

            print("\n=== EXECUTING GOAL ===")

            return self.goal_executor.execute(
                goal_plan,
            )

        except Exception as error:
            print("=" * 60)
            print("GOAL ORCHESTRATOR FAILED")
            print("=" * 60)

            print("ERROR:", error)

            return False, str(error)