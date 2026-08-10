from ai.tools.tool_registry import ToolRegistry
from desktop_automation.tools.desktop_tools import (
    register_desktop_tools,
)


def main():
    print("\n=== DESKTOP TOOL REGISTRATION TEST ===\n")

    registry = ToolRegistry()

    register_desktop_tools(registry)

    print("Registered desktop tools:\n")

    for tool in registry.all():
        print(f"- {tool.name}: {tool.description}")


if __name__ == "__main__":
    main()