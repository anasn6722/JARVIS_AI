from ai.reasoning.decision import Decision


class ReasoningEngine:
    BUILTIN_INTENTS = {
        "hello",
        "time",
        "identity",
        "set_name",
        "get_name",
        "set_preference",
        "get_preference",
        "last_message",
        "history",
    }

    PLANNER_INTENTS = {
        # Applications / websites
        "open",
        "close",
        "search",
        "youtube_search",

        # Desktop windows
        "focus_window",
        "close_window",
        "close_active_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "active_window",
        "list_windows",

        # Keyboard
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
    }

    def __init__(self, brain):
        self.brain = brain

    def decide(self, command):
        intent = command.intent

        # -------------------------
        # Built-in
        # -------------------------

        if intent in self.BUILTIN_INTENTS:
            route = "BUILTIN"

        # -------------------------
        # Planner
        # -------------------------

        elif intent in self.PLANNER_INTENTS:
            route = "PLANNER"

        # -------------------------
        # Plugins
        # -------------------------

        elif command.destination == "PLUGIN":
            route = "PLUGIN"

        # -------------------------
        # AI Chat
        # -------------------------

        else:
            route = "AI"

        return Decision(
            route=route,
            intent=intent,
        )