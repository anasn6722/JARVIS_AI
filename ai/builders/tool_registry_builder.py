
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from desktop_automation.controller.desktop_controller import DesktopController


class ToolRegistryBuilder:

    @staticmethod
    def build(brain):

        brain.tool_registry = ToolRegistry()

        brain.tool_executor = ToolExecutor(
            brain.tool_registry
        )

        # -------------------------
        # Desktop Automation
        # -------------------------

        brain.desktop = DesktopController()

        # -------------------------
        # Applications
        # -------------------------

        brain.tool_registry.register(
            "open",
            "Open any application",
            brain.app_handler.open,
        )

        brain.tool_registry.register(
            "close",
            "Close any application",
            brain.app_handler.close,
        )

        brain.tool_registry.register(
            "close_last",
            "Close last opened application",
            brain.app_handler.close_last,
        )

        # -------------------------
        # Desktop Windows
        # -------------------------

        brain.tool_registry.register(
            "list_windows",
            "List visible desktop windows",
            brain.desktop.list_windows,
        )

        brain.tool_registry.register(
            "active_window",
            "Get the currently active window",
            brain.desktop.active_window,
        )

        brain.tool_registry.register(
            "focus_window",
            "Focus a desktop window",
            brain.desktop.focus_window,
        )

        brain.tool_registry.register(
            "close_window",
            "Close a specific desktop window",
            brain.desktop.close_window,
        )

        brain.tool_registry.register(
            "close_active_window",
            "Close the currently active desktop window",
            brain.desktop.close_active_window,
        )

        # -------------------------
        # Web
        # -------------------------

        brain.tool_registry.register(
            "search",
            "Search Google",
            brain.handle_search,
        )

        brain.tool_registry.register(
            "youtube_search",
            "Search YouTube",
            brain.handle_youtube,
        )

        # -------------------------
        # Built-ins
        # -------------------------

        brain.tool_registry.register(
            "time",
            "Current time",
            brain.handle_time,
        )

        brain.tool_registry.register(
            "identity",
            "Who are you",
            brain.handle_identity,
        )

        return brain.tool_registry
