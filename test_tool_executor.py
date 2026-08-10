from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_loader import create_tool_registry


def main():
    print("\n=== TOOL EXECUTOR END-TO-END TEST ===\n")

    registry = create_tool_registry()
    executor = ToolExecutor(registry)

    print("Executing: active_window\n")

    result = executor.execute("active_window")

    print("RESULT:")
    print(result)

    print("\nExecuting: list_windows\n")

    result = executor.execute("list_windows")

    print("RESULT:")
    print(result)


if __name__ == "__main__":
    main()