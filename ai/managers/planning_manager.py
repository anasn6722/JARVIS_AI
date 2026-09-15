from collections.abc import Callable

from ai.agent.ai_planner import AIPlanner
from ai.agent.task import Task


class PlanningManager:
    """
    Coordinates rule-based planners and AI planning fallback.

    LOCAL / DESKTOP AUTOMATION:
        - Rule-based planning only.
        - Never falls back to Gemini.
        - If no local planner matches, return an explicit failed task.

    AI / GENERAL REQUESTS:
        - Rule-based planners are tried first.
        - Gemini planning is allowed as fallback.
    """

    # ============================================================
    # LOCAL / OFFLINE ACTIONS
    # ============================================================

    LOCAL_ACTIONS = {
        # Applications
        "open",
        "close",
        "close_last",

        # Windows
        "list_windows",
        "active_window",
        "find_window",
        "focus_window",
        "close_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",

        # Mouse
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",

        # Keyboard
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",

        # UI automation
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
        "open_search_result",

        # Filesystem
        "path_exists",
        "list_directory",
        "file_info",
        "create_folder",
        "create_file",
        "read_file",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",

        # Local built-ins
        "time",
        "identity",

        # Local web/search tools
        "search",
        "youtube_search",

        # Language switching
        "voice_language",
    }

    def __init__(
        self,
        planner_registry,
        ai_planner: AIPlanner,
        available_tools_provider: Callable[[], object],
        planner_context_provider: Callable[[], object],
    ):
        self.registry = planner_registry
        self.ai_planner = ai_planner
        self.available_tools_provider = available_tools_provider
        self.planner_context_provider = planner_context_provider

    # ============================================================
    # MAIN PLANNING
    # ============================================================

    def plan(self, command):
        """
        Create tasks for a command.

        1. Try rule-based planners.
        2. Local command + no planner:
           create explicit failed local task.
           NEVER call Gemini.
        3. Genuine AI command + no planner:
           allow AIPlanner/Gemini fallback.
        """

        intent = self._get_intent(command)

        print("=" * 50)
        print("PLANNING MANAGER")
        print(f"Intent: {intent}")
        print("=" * 50)

        # --------------------------------------------------------
        # RULE-BASED PLANNING
        # --------------------------------------------------------

        tasks = self.registry.plan(command)

        if tasks:
            print("Rule-based planner matched.")
            return tasks

        # --------------------------------------------------------
        # LOCAL OFFLINE FIREWALL
        # --------------------------------------------------------

        if self._is_local_action(intent):
            error = (
                f"No offline planner is registered for local action "
                f"'{intent}'."
            )

            print("=" * 50)
            print("OFFLINE PLANNING FIREWALL")
            print(f"Local action '{intent}' has no rule-based planner.")
            print("AI planning is BLOCKED.")
            print("Desktop/local automation remains 100% OFFLINE.")
            print(f"Planning error: {error}")
            print("=" * 50)

            # Create an explicit failed LOCAL task.
            #
            # This prevents the pipeline from treating the request
            # as if nothing happened. The normal verification and
            # recovery stages can now process the failure.
            failed_task = Task(
                action=intent,
                target=getattr(command, "original", None),
                max_retries=0,
            )

            failed_task.success = False
            failed_task.error = error
            failed_task.result = error

            return [failed_task]

        # --------------------------------------------------------
        # AI PLANNER FALLBACK
        # --------------------------------------------------------

        print("=" * 50)
        print("AI PLANNER FALLBACK")
        print(f"Intent '{intent}' is not a registered local action.")
        print("AI planning is allowed.")
        print("=" * 50)

        tasks = self.ai_planner.plan(
            command.original,
            self.available_tools_provider(),
            self.planner_context_provider(),
        )

        return tasks or []

    # ============================================================
    # HELPERS
    # ============================================================

    @classmethod
    def _is_local_action(cls, intent):
        if not isinstance(intent, str):
            return False

        return intent.strip().lower() in cls.LOCAL_ACTIONS

    @staticmethod
    def _get_intent(command):
        intent = getattr(command, "intent", None)

        if intent is None:
            return ""

        return str(intent).strip().lower()
