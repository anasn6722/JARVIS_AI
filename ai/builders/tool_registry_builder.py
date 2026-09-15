from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry
from desktop_automation.handler.desktop_handler import (
    DesktopHandler,
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

        brain.desktop_handler = DesktopHandler()

        # =================================================
        # APPLICATIONS
        # =================================================

        brain.tool_registry.register(
            "open",
            "Open an application, Windows component, or website.",
            brain.app_handler.open,
        )

        brain.tool_registry.register(
            "close",
            "Close an application.",
            brain.app_handler.close,
        )

        brain.tool_registry.register(
            "close_last",
            "Close the most recently referenced application or website.",
            brain.app_handler.close_last,
        )

        # =================================================
        # WINDOWS
        # =================================================

        brain.tool_registry.register(
            "list_windows",
            "List all visible desktop windows.",
            lambda target=None: brain.desktop_handler.handle(
                "list_windows"
            ),
        )

        brain.tool_registry.register(
            "active_window",
            "Get the currently active desktop window.",
            lambda target=None: brain.desktop_handler.handle(
                "active_window"
            ),
        )

        brain.tool_registry.register(
            "find_window",
            "Find a desktop window by name.",
            lambda target: brain.desktop_handler.handle(
                "find_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "focus_window",
            "Bring a desktop window to the foreground.",
            lambda target: brain.desktop_handler.handle(
                "focus_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "close_window",
            "Close a desktop window.",
            lambda target: brain.desktop_handler.handle(
                "close_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "minimize_window",
            "Minimize a desktop window.",
            lambda target: brain.desktop_handler.handle(
                "minimize_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "maximize_window",
            "Maximize a desktop window.",
            lambda target: brain.desktop_handler.handle(
                "maximize_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "restore_window",
            "Restore a desktop window.",
            lambda target: brain.desktop_handler.handle(
                "restore_window",
                target,
            ),
        )

        brain.tool_registry.register(
            "minimize_active_window",
            "Minimize the currently active window.",
            lambda target=None: brain.desktop_handler.handle(
                "minimize_active_window"
            ),
        )

        brain.tool_registry.register(
            "maximize_active_window",
            "Maximize the currently active window.",
            lambda target=None: brain.desktop_handler.handle(
                "maximize_active_window"
            ),
        )

        brain.tool_registry.register(
            "restore_active_window",
            "Restore the currently active window.",
            lambda target=None: brain.desktop_handler.handle(
                "restore_active_window"
            ),
        )

        # =================================================
        # MOUSE
        # =================================================

        brain.tool_registry.register(
            "mouse_position",
            "Get the current mouse cursor position.",
            lambda target=None: brain.desktop_handler.handle(
                "mouse_position"
            ),
        )

        brain.tool_registry.register(
            "mouse_move",
            "Move the mouse cursor to x,y coordinates.",
            lambda target: brain.desktop_handler.handle(
                "mouse_move",
                target,
            ),
        )

        brain.tool_registry.register(
            "mouse_click",
            "Left-click at coordinates or current position.",
            lambda target=None: brain.desktop_handler.handle(
                "mouse_click",
                target,
            ),
        )

        brain.tool_registry.register(
            "mouse_double_click",
            "Double-click at coordinates or current position.",
            lambda target=None: brain.desktop_handler.handle(
                "mouse_double_click",
                target,
            ),
        )

        brain.tool_registry.register(
            "mouse_right_click",
            "Right-click at coordinates or current position.",
            lambda target=None: brain.desktop_handler.handle(
                "mouse_right_click",
                target,
            ),
        )

        brain.tool_registry.register(
            "mouse_middle_click",
            "Middle-click at coordinates or current position.",
            lambda target=None: brain.desktop_handler.handle(
                "mouse_middle_click",
                target,
            ),
        )

        brain.tool_registry.register(
            "mouse_scroll",
            "Scroll vertically.",
            lambda target: brain.desktop_handler.handle(
                "mouse_scroll",
                target,
            ),
        )

        # =================================================
        # KEYBOARD
        # =================================================

        brain.tool_registry.register(
            "keyboard_type",
            "Type text into the currently focused application.",
            lambda target: brain.desktop_handler.handle(
                "keyboard_type",
                target,
            ),
        )

        brain.tool_registry.register(
            "keyboard_press",
            "Press a keyboard key.",
            lambda target: brain.desktop_handler.handle(
                "keyboard_press",
                target,
            ),
        )

        brain.tool_registry.register(
            "keyboard_hotkey",
            "Press a keyboard shortcut such as ctrl+a or alt+tab.",
            lambda target: brain.desktop_handler.handle(
                "keyboard_hotkey",
                target,
            ),
        )

        # =================================================
        # UI AUTOMATION
        # =================================================

        brain.tool_registry.register(
            "ui_find",
            "Find a visible UI element by name.",
            lambda target: brain.desktop_handler.handle(
                "ui_find",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_click",
            "Find a visible UI element and click it.",
            lambda target: brain.desktop_handler.handle(
                "ui_click",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_find_descriptor",
            "Find a UI element and return its semantic descriptor.",
            lambda target: brain.desktop_handler.handle(
                "ui_find_descriptor",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_click_descriptor",
            "Re-resolve and click a semantic UI descriptor.",
            lambda target: brain.desktop_handler.handle(
                "ui_click_descriptor",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_type_descriptor",
            "Re-resolve a semantic UI descriptor and type text.",
            lambda target: brain.desktop_handler.handle(
                "ui_type_descriptor",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_focus",
            "Find a visible UI element and focus it.",
            lambda target: brain.desktop_handler.handle(
                "ui_focus",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_click_at",
            "Find the UI element at x,y coordinates and click it.",
            lambda target: brain.desktop_handler.handle(
                "ui_click_at",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_describe",
            "Describe a visible UI element.",
            lambda target: brain.desktop_handler.handle(
                "ui_describe",
                target,
            ),
        )

        brain.tool_registry.register(
            "ui_type",
            "Focus a UI element and type text.",
            lambda target: brain.desktop_handler.handle(
                "ui_type",
                target,
            ),
        )

        # =================================================
        # DESKTOP SEARCH
        # =================================================

        brain.tool_registry.register(
            "search_ui",
            "Search the current desktop application.",
            lambda target: brain.desktop_handler.handle(
                "search_ui",
                target,
            ),
        )

        brain.tool_registry.register(
            "open_search_result",
            "Open a numbered search result.",
            lambda target: brain.desktop_handler.handle(
                "open_search_result",
                target,
            ),
        )

        # =================================================
        # FILESYSTEM AUTOMATION
        # =================================================

        brain.tool_registry.register(
            "path_exists",
            "Check whether a file or folder exists.",
            lambda target: brain.desktop_handler.handle(
                "path_exists",
                target,
            ),
        )

        brain.tool_registry.register(
            "list_directory",
            "List files and folders in a directory.",
            lambda target: brain.desktop_handler.handle(
                "list_directory",
                target,
            ),
        )

        brain.tool_registry.register(
            "file_info",
            "Get information about a file or folder.",
            lambda target: brain.desktop_handler.handle(
                "file_info",
                target,
            ),
        )

        brain.tool_registry.register(
            "create_folder",
            "Create a folder.",
            lambda target: brain.desktop_handler.handle(
                "create_folder",
                target,
            ),
        )

        brain.tool_registry.register(
            "create_file",
            "Create a text file with optional content.",
            lambda target: brain.desktop_handler.handle(
                "create_file",
                target,
            ),
        )

        brain.tool_registry.register(
            "read_file",
            "Read a text file.",
            lambda target: brain.desktop_handler.handle(
                "read_file",
                target,
            ),
        )

        brain.tool_registry.register(
            "copy",
            "Copy a file or folder.",
            lambda target: brain.desktop_handler.handle(
                "copy",
                target,
            ),
        )

        brain.tool_registry.register(
            "move",
            "Move a file or folder.",
            lambda target: brain.desktop_handler.handle(
                "move",
                target,
            ),
        )

        brain.tool_registry.register(
            "rename",
            "Rename a file or folder.",
            lambda target: brain.desktop_handler.handle(
                "rename",
                target,
            ),
        )

        brain.tool_registry.register(
            "search_files",
            "Search for files or folders.",
            lambda target: brain.desktop_handler.handle(
                "search_files",
                target,
            ),
        )

        brain.tool_registry.register(
            "open_path",
            "Open a file or folder with its default application.",
            lambda target: brain.desktop_handler.handle(
                "open_path",
                target,
            ),
        )

        brain.tool_registry.register(
            "open_in_explorer",
            "Open a file or folder in File Explorer.",
            lambda target: brain.desktop_handler.handle(
                "open_in_explorer",
                target,
            ),
        )

        # =================================================
        # WEB
        # =================================================

        brain.tool_registry.register(
            "search",
            "Search Google.",
            brain.handle_search,
        )

        brain.tool_registry.register(
            "youtube_search",
            "Search YouTube.",
            brain.handle_youtube,
        )

        # =================================================
        # BUILT-INS
        # =================================================

        brain.tool_registry.register(
            "time",
            "Get the current time.",
            brain.handle_time,
        )

        brain.tool_registry.register(
            "identity",
            "Identify JARVIS.",
            brain.handle_identity,
        )

        return brain.tool_registry
