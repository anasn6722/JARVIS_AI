from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class DesktopAgent(BaseAgent):
    """Handles Windows desktop and UI automation."""

    name = "desktop"
    description = (
        "Handles applications, windows, mouse, keyboard, "
        "and desktop UI automation."
    )

    DESKTOP_INTENTS = {
        "open",
        "close",
        "close_last",
        "focus_window",
        "list_windows",
        "active_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "search_ui",
    }

    def can_handle(self, command):
        return command.intent in self.DESKTOP_INTENTS

    def run(self, context):
        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "delegate_to_existing_pipeline": True,
            },
        )