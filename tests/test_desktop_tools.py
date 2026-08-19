
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from desktop_automation.controller.desktop_controller import DesktopController


def main():
    registry = ToolRegistry()

    desktop = DesktopController()

    registry.register(
        "list_windows",
        "List visible desktop windows",
        desktop.list_windows,
    )

    registry.register(
        "active_window",
        "Get active desktop window",
        desktop.active_window,
    )

    registry.register(
        "focus_window",
        "Focus desktop window",
        desktop.focus_window,
    )

    executor = ToolExecutor(registry)

    print("\n=== ACTIVE WINDOW ===\n")

    result = executor.execute(
        "active_window"
    )

    print(result)

    print("\n=== FIND VS CODE ===\n")

    result = executor.execute(
        "focus_window",
        "visual studio code",
    )

    print(result)


if __name__ == "__main__":
    main()
