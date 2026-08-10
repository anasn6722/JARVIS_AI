from ai.agent.goal_ai_planner import GoalAIPlanner
from ai.agent.goal_decomposer import GoalDecomposer
from ai.agent.goal_executor import GoalExecutor
from ai.agent.goal_orchestrator import GoalOrchestrator
from ai.llm.llm import LLM
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
    )

    # --------------------------------------------------------
    # GOAL ORCHESTRATOR
    # --------------------------------------------------------

    orchestrator = GoalOrchestrator(
        goal_decomposer,
        goal_executor,
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


if __name__ == "__main__":
    main()