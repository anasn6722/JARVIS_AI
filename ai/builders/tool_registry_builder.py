from ai.tools.tool_executor import ToolExecutor
from ai.tools.tool_registry import ToolRegistry


class ToolRegistryBuilder:

    @staticmethod
    def build(brain):

        brain.tool_registry = ToolRegistry()

        brain.tool_executor = ToolExecutor(
            brain.tool_registry
        )

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