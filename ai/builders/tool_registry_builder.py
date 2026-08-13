
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
            brain.desktop.get_active_window,
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
        # MOUSE AUTOMATION
        # =================================================

        brain.tool_registry.register(
            "mouse_position",
            "Get the current mouse cursor position.",
            brain.desktop.mouse_position,
        )

        brain.tool_registry.register(
            "mouse_move",
            "Move the mouse cursor to x,y coordinates.",
            brain.desktop.mouse_move,
        )

        brain.tool_registry.register(
            "mouse_click",
            "Left-click at x,y coordinates or current position.",
            brain.desktop.mouse_click,
        )

        brain.tool_registry.register(
            "mouse_double_click",
            "Double-click at x,y coordinates or current position.",
            brain.desktop.mouse_double_click,
        )

        brain.tool_registry.register(
            "mouse_right_click",
            "Right-click at x,y coordinates or current position.",
            brain.desktop.mouse_right_click,
        )

        brain.tool_registry.register(
            "mouse_middle_click",
            "Middle-click at x,y coordinates or current position.",
            brain.desktop.mouse_middle_click,
        )

        brain.tool_registry.register(
            "mouse_scroll",
            "Scroll vertically. Positive values scroll up; negative values scroll down.",
            brain.desktop.mouse_scroll,
        )

        # =================================================
        # KEYBOARD AUTOMATION
        # =================================================
        
        brain.tool_registry.register(
            "keyboard_type",
            "Type text into the currently focused application.",
            brain.desktop.keyboard_type,
        )
        
        brain.tool_registry.register(
            "keyboard_press",
            "Press a keyboard key.",
            brain.desktop.keyboard_press,
        )
        
        brain.tool_registry.register(
            "keyboard_hotkey",
            "Press a keyboard shortcut such as ctrl+a, ctrl+c, or alt+tab.",
            brain.desktop.keyboard_hotkey,
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
