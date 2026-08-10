from datetime import datetime

from ai.memory.goal_execution import GoalExecution
from ai.memory.goal_execution_memory import GoalExecutionMemory


def main():
    print("=== JARVIS GOAL EXECUTION MEMORY TEST ===")

    memory = GoalExecutionMemory(
        "data/test_goal_execution_history.json",
    )

    memory.clear()

    print("\n=== ADD EXECUTIONS ===")

    first = GoalExecution(
        goal_id="goal-001",
        action="get_system_info",
        target="desktop",
        started=datetime.now(),
        completed=datetime.now(),
        success=True,
        result="Windows 11",
    )

    second = GoalExecution(
        goal_id="goal-001",
        action="get_display_info",
        target="display",
        started=datetime.now(),
        completed=datetime.now(),
        success=True,
        result="1280x720",
    )

    memory.add(first)
    memory.add(second)

    print(
        "Executions stored:",
        len(memory.all()),
    )

    print("\n=== BY GOAL ===")

    executions = memory.by_goal(
        "goal-001",
    )

    for execution in executions:
        print(
            execution.action,
            "->",
            execution.result,
        )

    print("\n=== RELOAD ===")

    reloaded = GoalExecutionMemory(
        "data/test_goal_execution_history.json",
    )

    print(
        "Loaded:",
        len(reloaded.all()),
    )

    for execution in reloaded.all():
        print(
            execution.action,
            "->",
            execution.result,
        )

    print("\n=== CLEAR ===")

    reloaded.clear()

    print(
        "Remaining:",
        len(reloaded.all()),
    )

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()
