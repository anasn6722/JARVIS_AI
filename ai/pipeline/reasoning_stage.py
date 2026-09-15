from dataclasses import replace

# ============================================================
# LOCAL / OFFLINE COMMANDS
# ============================================================
#
# These commands must NEVER be sent to Gemini.
#
# They are handled locally by:
#   CommandStage
#       ↓
#   ReasoningStage
#       ↓
#   PlanningStage
#       ↓
#   Local Tool
#
# ============================================================

LOCAL_INTENTS = {
    # -----------------------------
    # APPLICATION CONTROL
    # -----------------------------
    "open",
    "close",
    "close_last",

    # -----------------------------
    # WINDOW CONTROL
    # -----------------------------
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

    # -----------------------------
    # MOUSE
    # -----------------------------
    "mouse_position",
    "mouse_move",
    "mouse_click",
    "mouse_double_click",
    "mouse_right_click",
    "mouse_middle_click",
    "mouse_scroll",

    # -----------------------------
    # KEYBOARD
    # -----------------------------
    "keyboard_type",
    "keyboard_press",
    "keyboard_hotkey",

    # -----------------------------
    # UI AUTOMATION
    # -----------------------------
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

    # -----------------------------
    # FILESYSTEM
    # -----------------------------
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

    # -----------------------------
    # LOCAL INFORMATION
    # -----------------------------
    "time",
    "identity",

    # -----------------------------
    # VOICE / LANGUAGE
    # -----------------------------
    "voice_language",
}


class ReasoningStage:
    def __init__(self, brain):
        self.brain = brain

    # ============================================================
    # LOCAL DECISION
    # ============================================================

    @staticmethod
    def _local_decision(command):
        """
        Build a planner decision directly from the already
        canonicalized local command.

        IMPORTANT:
        Do NOT call the LLM/reasoning engine here.
        """

        # Preserve the existing decision object's class/API
        # without relying on a specific import path.
        #
        # This works with the current Decision object because
        # its constructor accepts:
        # route, intent, confidence, tool, reason
        #
        # Import lazily to avoid startup/import-order issues.
        try:
            from ai.reasoning.decision import Decision
        except ImportError:
            try:
                from ai.reasoning import Decision
            except ImportError:
                Decision = None

        if Decision is None:
            raise ImportError(
                "Could not import Decision. "
                "Expected ai.reasoning.decision.Decision "
                "or ai.reasoning.Decision."
            )

        return Decision(
            route="PLANNER",
            intent=command.intent,
            confidence=getattr(command, "confidence", 1.0) or 1.0,
            tool=None,
            reason="Registered local command; handled offline.",
        )

    # ============================================================
    # RUN
    # ============================================================

    def run(self, context):

        context.decisions = []
        context.decision = None

        for item in context.commands:

            command = item["command"]

            # Normalize intent safely.
            intent = str(
                getattr(command, "intent", "") or ""
            ).strip().lower()

            # ====================================================
            # LOCAL-FIRST GATE
            # ====================================================
            #
            # Any registered local intent is authoritative.
            #
            # We DO NOT ask the general reasoning engine to
            # reinterpret it.
            # ====================================================

            if intent in LOCAL_INTENTS:

                decision = self._local_decision(command)

                print(
                    f"LOCAL-FIRST: intent='{intent}' "
                    f"→ route='PLANNER' "
                    f"(OFFLINE)"
                )

            else:

                # =================================================
                # NON-LOCAL COMMAND
                # =================================================
                #
                # Unknown/general commands continue through the
                # normal reasoning system.
                # =================================================

                decision = self.brain.reasoning.decide(command)

            # ====================================================
            # STORE DECISION
            # ====================================================

            context.decisions.append(
                {
                    "command": command,
                    "decision": decision,
                }
            )

            # Keep current decision for downstream stages.
            context.decision = decision

            print("=" * 50)
            print("REASONING")
            print(decision)
            print("=" * 50)