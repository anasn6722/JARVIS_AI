from ai.agent.goal import Goal
from ai.agent.goal_plan import GoalPlan
from ai.planning.goal_graph_builder import GoalGraphBuilder


class GoalDecomposer:
    """Convert a goal into tasks and an execution graph."""

    def __init__(
        self,
        goal_ai_planner,
        task_parser,
    ):
        self.goal_ai_planner = goal_ai_planner
        self.task_parser = task_parser
        self.graph_builder = GoalGraphBuilder()

    def decompose(
        self,
        goal_text,
    ):
        raw_tasks = self.goal_ai_planner.create_plan(
            goal_text,
        )

        tasks = self.task_parser.parse(
            raw_tasks,
        )

        graph = self.graph_builder.build(
            tasks,
        )
        
        goal = Goal(
            id="goal_001",
            title=goal_text,
            description=goal_text,
            tasks=tasks,
        )
        
        return GoalPlan(
            goal=goal,
            graph=graph,
        )