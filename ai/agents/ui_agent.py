from ai.agents.base_agent import BaseAgent
from ai.orchestration.agent_result import AgentResult


class UIAgent(BaseAgent):
    """Controls the JARVIS application interface."""

    name = "ui"
    description = (
        "Controls JARVIS internal pages, navigation, "
        "HUD interface, and application UI."
    )

    PAGE_ALIASES = {
        "dashboard": 0,
        "command center": 0,
        "command centre": 0,
        "command":0,    
        "home": 0,

        "chat": 1,
        "chat console": 1,

        "voice": 2,
        "voice interface": 2,
        "voice core": 2,

        "memory": 3,
        "memory core": 3,

        "settings": 4,
        "system settings": 4,
    }

    UI_INTENTS = {
        "navigate",
        "ui_find",
        "ui_click",
        "ui_focus",
        "ui_describe",
    }

    def can_handle(self, command):
        if command.intent in self.UI_INTENTS:
            return True

        text = command.original.lower().strip()

        return any(
            phrase in text
            for phrase in (
                "open dashboard",
                "open command center",
                "open command centre",
                "open chat",
                "open chat console",
                "open voice",
                "open voice interface",
                "open voice core",
                "open memory",
                "open memory core",
                "open settings",
                "open system settings",
                "go to command center",
                "go to command centre",
                "go to chat",
                "go to voice",
                "go to memory",
                "go to settings",
                "show command center",
                "show command centre",
            )
        )

    def resolve_page(self, command):
        text = command.original.lower().strip()

        for alias, index in self.PAGE_ALIASES.items():
            if alias in text:
                return index

        return None

    def run(self, context):
        page_index = self.resolve_page(
            context.command
        )

        if page_index is None:
            return AgentResult(
                success=True,
                agent=self.name,
                metadata={
                    "delegate_to_existing_pipeline": True,
                },
            )

        return AgentResult(
            success=True,
            agent=self.name,
            metadata={
                "internal_navigation": True,
                "page_index": page_index,
            },
        )