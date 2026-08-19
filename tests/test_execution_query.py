from ai.memory.execution.execution_history import ExecutionHistory
from ai.memory.execution.execution_memory import ExecutionMemory
from ai.memory.execution.execution_query import ExecutionQuery


def main():
    print("=== JARVIS EXECUTION QUERY TEST ===")

    memory = ExecutionMemory()

    history = ExecutionHistory(
        memory,
    )

    query = ExecutionQuery(
        history,
    )

    print("\n=== LAST ===")

    last = query.last()

    if last:
        print(
            last.action,
            "->",
            last.success,
        )
    else:
        print("No executions found.")

    print("\n=== RECENT ===")

    for execution in query.recent(3):
        print(
            execution.action,
            "->",
            execution.success,
        )

    print("\n=== SUCCESSFUL ===")

    for execution in query.successful():
        print(execution.action)

    print("\n=== FAILED ===")

    for execution in query.failed():
        print(
            execution.action,
            "->",
            execution.error,
        )

    print("\n=== SUMMARY ===")

    print(
        query.summary(),
    )

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()