from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class DesktopAgent(BaseAgent):
    """Handles Windows desktop, UI, application, and filesystem automation."""

    name = "desktop"
    description = (
        "Handles applications, windows, mouse, keyboard, "
        "desktop UI automation, files, folders, and filesystem operations."
    )

    DESKTOP_INTENTS = {
        # =====================================================
        # APPLICATIONS
        # =====================================================

        "open",
        "close",
        "close_last",

        # =====================================================
        # WINDOWS
        # =====================================================

        "focus_window",
        "close_window",
        "close_active_window",
        "list_windows",
        "active_window",
        "find_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",

        # =====================================================
        # MOUSE
        # =====================================================

        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "mouse_scroll_up",
        "mouse_scroll_down",

        # =====================================================
        # KEYBOARD
        # =====================================================

        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",

        # =====================================================
        # SEMANTIC UI
        # =====================================================

        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",

        # =====================================================
        # DESKTOP SEARCH
        # =====================================================

        "search_ui",
        "open_search_result",

        # =====================================================
        # FILESYSTEM
        # =====================================================

        "path_exists",
        "list_directory",
        "create_folder",
        "create_file",
        "read_file",
        "file_info",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",
    }

    def can_handle(self, command):
        """Return True when this agent can handle the command."""

        if command is None:
            return False

        return (
            getattr(command, "intent", None)
            in self.DESKTOP_INTENTS
        )

    def run(self, context):
        """
        Delegate the actual work to the existing JARVIS
        planning/execution pipeline.
        """

        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
            },
        )
