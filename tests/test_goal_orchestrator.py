from ai.agent.goal_ai_planner import GoalAIPlanner
from ai.agent.goal_decomposer import GoalDecomposer
from ai.agent.goal_executor import GoalExecutor
from ai.agent.goal_orchestrator import GoalOrchestrator
from ai.goal_manager import GoalManager
from ai.llm.llm import LLM
from ai.memory.goal_memory import GoalMemory
from ai.planner.task_parser import TaskParser
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_loader import create_tool_registry
from ai.workflow.workflow_manager import WorkflowManager


def main():
    print("=" * 60)
    print("JARVIS GOAL ORCHESTRATOR TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # BUILD TOOL REGISTRY
    # --------------------------------------------------------

    print("\n=== BUILDING TOOL REGISTRY ===")

    registry = create_tool_registry()

    print("\nRegistered tools:")

    for tool in registry.all():
        print(f"- {tool.name}")

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
    # GOAL MEMORY
    # --------------------------------------------------------

    goal_memory = GoalMemory()

    # --------------------------------------------------------
    # GOAL MANAGER
    # --------------------------------------------------------

    goal_manager = GoalManager(
        goal_memory,
    )

    # --------------------------------------------------------
    # GOAL PLANNER
    # --------------------------------------------------------

    llm = LLM()

    goal_ai_planner = GoalAIPlanner(
        llm,
        registry,
    )

    task_parser = TaskParser()

    goal_decomposer = GoalDecomposer(
        goal_ai_planner,
        task_parser,
    )

    # --------------------------------------------------------
    # GOAL EXECUTOR
    # --------------------------------------------------------

    goal_executor = GoalExecutor(
        workflow_manager,
        goal_manager,
    )

    # --------------------------------------------------------
    # GOAL ORCHESTRATOR
    # --------------------------------------------------------

    orchestrator = GoalOrchestrator(
        goal_decomposer,
        goal_executor,
        goal_manager,
    )

    # --------------------------------------------------------
    # EXECUTE GOAL
    # --------------------------------------------------------

    goal = "Show my current desktop information"

    print("\n=== EXECUTING GOAL ===")
    print("Goal:", goal)

    success, response = orchestrator.execute(
        goal,
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print("\n=== RESULT ===")

    print("Success:", success)

    print("Response:")

    print(response)

    # --------------------------------------------------------
    # PERSISTENCE CHECK
    # --------------------------------------------------------

    print("\n=== SAVED GOALS ===")

    for saved_goal in goal_manager.all_goals():
        print(
            saved_goal.id,
            "->",
            saved_goal.title,
        )

        print(
            "State:",
            goal_manager.get_state(
                saved_goal.id,
            ),
        )

        print(
            "Progress:",
            saved_goal.progress,
        )

        print(
            "Completed:",
            saved_goal.completed,
        )


if __name__ == "__main__":
    main()
