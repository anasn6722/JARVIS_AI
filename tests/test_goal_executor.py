from ai.agent.goal_decomposer import GoalDecomposer
from ai.agent.goal_executor import GoalExecutor
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_loader import create_tool_registry
from ai.tools.tool_registry import ToolRegistry
from ai.workflow.workflow_manager import WorkflowManager
from desktop_automation.controller.desktop_controller import DesktopController


class MockGoalAIPlanner:
    """Temporary planner for integration testing."""

    def create_plan(self, goal_text):
        return [
            "show windows",
            "active window",
        ]


class MockTaskParser:
    """Temporary task parser for integration testing."""

    def parse(self, raw_tasks):
        from ai.agent.task import Task

        return [
            Task(
                action="list_windows",
            ),
            Task(
                action="active_window",
            ),
        ]


def build_registry():
    """Build the tool registry used by JARVIS."""

    registry = ToolRegistry()

    desktop = DesktopController()

    registry.register(
        name="list_windows",
        description="List visible desktop windows.",
        callback=desktop.list_windows,
    )

    registry.register(
        name="active_window",
        description="Get the currently active window.",
        callback=desktop.get_active_window,
    )

    registry = create_tool_registry()
    
    tool_executor = ToolExecutor(
        registry,
    )
    return registry


def main():
    print("=" * 60)
    print("JARVIS GOAL EXECUTION TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # TOOL REGISTRY
    # --------------------------------------------------------

    print("\n=== BUILDING TOOL REGISTRY ===")

    registry = build_registry()

    print("Registered tools:")

    for tool in registry.all():
        print(
            "-",
            tool.name,
        )

    # --------------------------------------------------------
    # TOOL EXECUTOR
    # --------------------------------------------------------

    tool_executor = ToolExecutor(
        registry,
    )

    # --------------------------------------------------------
    # WORKFLOW MANAGER
    # --------------------------------------------------------

    workflow_manager = WorkflowManager(
        tool_executor,
    )

    # --------------------------------------------------------
    # GOAL DECOMPOSER
    # --------------------------------------------------------

    goal_planner = MockGoalAIPlanner()
    task_parser = MockTaskParser()

    decomposer = GoalDecomposer(
        goal_ai_planner=goal_planner,
        task_parser=task_parser,
    )

    # --------------------------------------------------------
    # GOAL EXECUTOR
    # --------------------------------------------------------

    goal_executor = GoalExecutor(
        workflow_manager,
    )

    # --------------------------------------------------------
    # CREATE GOAL
    # --------------------------------------------------------

    print("\n=== DECOMPOSING GOAL ===")

    goal_plan = decomposer.decompose(
        "Show my current desktop information",
    )

    print(
        "Goal:",
        goal_plan.goal.title,
    )

    print("\nTasks:")

    for task in goal_plan.goal.tasks:
        print(
            "-",
            task.action,
            "→",
            task.target,
        )

    # --------------------------------------------------------
    # EXECUTE GOAL
    # --------------------------------------------------------

    print("\n=== EXECUTING GOAL ===")

    success, response = goal_executor.execute(
        goal_plan,
    )

    print("\n=== RESULT ===")

    print(
        "Success:",
        success,
    )

    print(
        "Response:",
    )

    print(
        response,
    )

    print(
        "\nGoal completed:",
        goal_plan.goal.completed,
    )


if __name__ == "__main__":
    main()