from datetime import datetime
from uuid import uuid4

from ai.agent.goal_decomposer import GoalDecomposer
from ai.agent.goal_executor import GoalExecutor
from ai.memory.goal_record import GoalRecord


class GoalOrchestrator:
    """Coordinate goal planning, persistence, and execution."""

    def __init__(
        self,
        goal_decomposer: GoalDecomposer,
        goal_executor: GoalExecutor,
        goal_manager=None,
    ):
        self.goal_decomposer = goal_decomposer
        self.goal_executor = goal_executor
        self.goal_manager = goal_manager

    def execute(self, goal_text):
        """Decompose, persist, and execute a natural-language goal."""

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
            # ====================================================
            # DECOMPOSE
            # ====================================================

            print("\n=== DECOMPOSING GOAL ===")

            goal_plan = self.goal_decomposer.decompose(
                goal_text,
            )

            if not goal_plan:
                return False, "Could not create a goal plan."

            planned_goal = goal_plan.goal

            print(
                "Goal:",
                planned_goal.title,
            )

            print(
                "Tasks:",
                len(planned_goal.tasks),
            )

            # ====================================================
            # PERSIST GOAL
            # ====================================================

            if self.goal_manager:
                persistent_goal = GoalRecord(
                    id=str(uuid4()),
                    title=planned_goal.title,
                    description=planned_goal.description,
                    created=datetime.now(),
                    tasks=planned_goal.tasks,
                )

                self.goal_manager.goal_memory.add(
                    persistent_goal,
                )

                print(
                    "Persistent Goal ID:",
                    persistent_goal.id,
                )

                # Keep the execution plan connected to the
                # persistent goal.
                goal_plan.goal = persistent_goal

            # ====================================================
            # EXECUTE
            # ====================================================

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
