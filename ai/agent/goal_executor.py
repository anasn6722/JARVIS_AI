from ai.agent.goal_plan import GoalPlan


class GoalExecutor:
    """Execute a decomposed goal through the workflow system."""

    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager

    def execute(self, goal_plan: GoalPlan):
        """Execute all tasks belonging to a goal plan."""

        if not goal_plan:
            return False, "No goal plan provided."

        goal = goal_plan.goal
        graph = goal_plan.graph

        if not graph:
            return False, "Goal plan has no task graph."

        print("=" * 60)
        print("GOAL EXECUTION START")
        print("=" * 60)

        print("Goal:", goal.title)

        try:
            response = self.workflow_manager.run(
                graph=graph,
            )

            goal.completed = True

            print("=" * 60)
            print("GOAL EXECUTION COMPLETED")
            print("=" * 60)

            return True, response

        except Exception as error:
            print("=" * 60)
            print("GOAL EXECUTION FAILED")
            print("=" * 60)

            print("ERROR:", error)

            return False, str(error)