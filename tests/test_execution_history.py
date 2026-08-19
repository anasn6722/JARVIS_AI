from ai.memory.execution.execution_history import ExecutionHistory
from ai.memory.execution.execution_memory import ExecutionMemory
from ai.memory.execution.execution_record import ExecutionRecord


def main():
    print("=== JARVIS EXECUTION HISTORY TEST ===")

    memory = ExecutionMemory()
    memory.clear()

    print("\n=== ADD EXECUTIONS ===")

    execution_1 = ExecutionRecord(
        goal_id="goal-001",
        action="get_system_info",
        target="desktop",
        success=True,
        result="Windows 11",
    )

    execution_2 = ExecutionRecord(
        goal_id="goal-001",
        action="get_display_info",
        target="display",
        success=True,
        result="1280x720",
    )

    execution_3 = ExecutionRecord(
        goal_id="goal-002",
        action="list_windows",
        target="desktop",
        success=False,
        result="",
        error="Window enumeration failed",
    )

    memory.add(execution_1)
    memory.add(execution_2)
    memory.add(execution_3)

    print("Executions:", len(memory.all()))

    history = ExecutionHistory(memory)

    print("\n=== BY GOAL ===")

    goal_executions = history.by_goal("goal-001")

    for execution in goal_executions:
        print(
            execution.action,
            "->",
            execution.result,
        )

    print("\n=== RECENT ===")

    for execution in history.recent(2):
        print(
            execution.action,
            "->",
            execution.success,
        )

    print("\n=== LAST ===")

    last = history.last()

    if last:
        print(
            last.action,
            "->",
            last.success,
        )

    print("\n=== SUCCESSFUL ===")

    for execution in history.successful():
        print(execution.action)

    print("\n=== FAILED ===")

    for execution in history.failed():
        print(
            execution.action,
            "->",
            execution.error,
        )

    
    print("\n=== BY ACTION ===")

    for execution in history.by_action(
        "get_system_info",
    ):
        print(
            execution.action,
            "->",
            execution.result,
        )

    print("\n=== TODAY ===")

    for execution in history.today():
        print(
            execution.action,
            "->",
            execution.success,
        )

    print("\n=== COUNTS ===")

    print(
        "Successful:",
        history.successful_count(),
    )

    print(
        "Failed:",
        history.failed_count(),
    )

    print("\n=== SUMMARY ===")

    print(history.summary())
    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()
