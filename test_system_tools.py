from ai.tools.tool_loader import create_tool_registry


def main():
    print("=" * 60)
    print("JARVIS SYSTEM TOOLS TEST")
    print("=" * 60)

    registry = create_tool_registry()

    print("\n=== SYSTEM INFO ===")

    system_tool = registry.get("get_system_info")

    if system_tool:
        print(system_tool.callback())

    print("\n=== DISPLAY INFO ===")

    display_tool = registry.get("get_display_info")

    if display_tool:
        print(display_tool.callback())

    print("\n=== ACTIVE PROCESSES ===")

    process_tool = registry.get(
        "list_active_processes"
    )

    if process_tool:
        processes = process_tool.callback()

        print(
            "Process count:",
            len(processes),
        )

        for process in processes[:10]:
            print(process)


if __name__ == "__main__":
    main()