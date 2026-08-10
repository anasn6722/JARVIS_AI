from ai.tools.system_tool_registration import register_system_tools
from ai.tools.tool_registry import ToolRegistry
from desktop_automation.tools.desktop_tools import register_desktop_tools


def create_tool_registry():
    """Create and populate the central JARVIS tool registry."""

    registry = ToolRegistry()

    register_desktop_tools(registry)
    register_system_tools(registry)

    return registry