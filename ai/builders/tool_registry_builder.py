
from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from desktop_automation.controller.desktop_controller import (
    DesktopController,
)


class ToolRegistryBuilder:
    """Build and register all JARVIS tools."""

    @staticmethod
    def build(brain):
        brain.tool_registry = ToolRegistry()

        brain.tool_executor = ToolExecutor(
            brain.tool_registry
        )

        # =================================================
        # DESKTOP AUTOMATION
        # =================================================

        brain.desktop = DesktopController()

        # =================================================
        # APPLICATIONS
        # =================================================

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

        # =================================================
        # DESKTOP WINDOWS
        # =================================================

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
            "minimize_window",
            "Minimize a desktop window",
            brain.desktop.minimize_window,
        )

        brain.tool_registry.register(
            "maximize_window",
            "Maximize a desktop window",
            brain.desktop.maximize_window,
        )

        brain.tool_registry.register(
            "restore_window",
            "Restore a desktop window",
            brain.desktop.restore_window,
        )

        brain.tool_registry.register(
            "minimize_active_window",
            "Minimize the currently active window",
            brain.desktop.minimize_active_window,
        )

        brain.tool_registry.register(
            "maximize_active_window",
            "Maximize the currently active window",
            brain.desktop.maximize_active_window,
        )

        brain.tool_registry.register(
            "restore_active_window",
            "Restore the currently active window",
            brain.desktop.restore_active_window,
        )

        # =================================================
        # WEB
        # =================================================

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

        # =================================================
        # BUILT-INS
        # =================================================

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
