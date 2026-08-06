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
        "open",
        "close",
        "search",
        "youtube_search",

        "add_goal",
        "show_goals",
        "next_task",
        "complete_task",
        "goal_progress",
        "delete_goal",
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