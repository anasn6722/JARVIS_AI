from ai.tools.system_tools import (
    get_display_info,
    get_system_info,
    list_active_processes,
)


def register_system_tools(registry):
    """Register system information tools."""

    registry.register(
        "get_system_info",
        "Get operating system and computer information.",
        get_system_info,
    )

    registry.register(
        "get_display_info",
        "Get screen and display information.",
        get_display_info,
    )

    registry.register(
        "list_active_processes",
        "List currently running applications and processes.",
        list_active_processes,
    )