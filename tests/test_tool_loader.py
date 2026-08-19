from ai.tools.tool_loader import create_tool_registry


def main():
    print("\n=== CENTRAL TOOL REGISTRY TEST ===\n")

    registry = create_tool_registry()

    print("All registered tools:\n")

    for tool in registry.all():
        print(f"- {tool.name}: {tool.description}")


if __name__ == "__main__":
    main()