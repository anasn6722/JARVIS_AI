
from ai.agent.goal_plan import GoalPlan
from ai.agent.goal_state import GoalState


class GoalExecutor:
    """Execute a decomposed goal through the workflow system."""

    def __init__(
        self,
        workflow_manager,
        goal_manager=None,
    ):
        self.workflow_manager = workflow_manager
        self.goal_manager = goal_manager

    def execute(self, goal_plan: GoalPlan):
        """Execute all tasks belonging to a goal plan."""

        if not goal_plan:
            return False, "No goal plan provided."

        goal = goal_plan.goal
        graph = goal_plan.graph

        if not graph:
            return False, "Goal plan has no task graph."

        # ========================================================
        # STATE CHECK
        # ========================================================

        if goal.archived:
            return False, "Cannot execute an archived goal."

        if goal.completed:
            return False, "Goal is already completed."

        if goal.paused:
            return False, "Goal is paused."

        # ========================================================
        # START GOAL
        # ========================================================

        goal.state = GoalState.RUNNING

        if self.goal_manager:
            self.goal_manager.goal_memory.save()

        print("=" * 60)
        print("GOAL EXECUTION START")
        print("=" * 60)

        print("Goal:", goal.title)
        print("State:", goal.state)

        try:
            # ====================================================
            # EXECUTE GRAPH
            # ====================================================

            response = self.workflow_manager.run(
                graph=graph,
            )

            # ====================================================
            # GRAPH FAILED
            # ====================================================

            if not graph.completed():
                return False, response

            # ====================================================
            # UPDATE TASK PROGRESS
            # ====================================================

            completed_tasks = sum(
                node.task.completed
                for node in graph.nodes
            )

            total_tasks = len(graph.nodes)

            if total_tasks:
                goal.progress = (
                    completed_tasks / total_tasks
                ) * 100.0

            # ====================================================
            # GOAL COMPLETED
            # ====================================================

            goal.completed = True
            goal.paused = False
            goal.progress = 100.0
            goal.state = GoalState.COMPLETED

            if self.goal_manager:
                self.goal_manager.goal_memory.save()

            print("=" * 60)
            print("GOAL EXECUTION COMPLETED")
            print("=" * 60)

            print("State:", goal.state)
            print("Progress:", goal.progress)

            return True, response

        except Exception as error:
            goal.state = GoalState.PENDING

            if self.goal_manager:
                self.goal_manager.goal_memory.save()

            print("=" * 60)
            print("GOAL EXECUTION FAILED")
            print("=" * 60)

            print("ERROR:", error)

            return False, str(error)
        