from ai.memory.execution.execution_context import ExecutionContext
from ai.memory.execution.execution_history import ExecutionHistory
from ai.memory.execution.execution_memory import ExecutionMemory
from ai.memory.execution.execution_query import ExecutionQuery


def main():
    print("=== JARVIS EXECUTION CONTEXT TEST ===")

    memory = ExecutionMemory()
    history = ExecutionHistory(memory)
    query = ExecutionQuery(history)
    context = ExecutionContext(query)

    print("\n=== RECENT CONTEXT ===")
    print(context.recent(5))

    print("\n=== LAST CONTEXT ===")
    print(context.last())

    print("\n=== SUMMARY CONTEXT ===")
    print(context.summary())

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()