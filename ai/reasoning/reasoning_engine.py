from ai.reasoning.decision import Decision


class ReasoningEngine:

    def __init__(self, brain):
        self.brain = brain

    def analyze(self, command):

        intent = command.intent

        if intent in (
            "get_preference",
            "set_preference",
            "get_name",
            "set_name",
        ):
            return Decision(
                route="MEMORY",
                intent=intent,
            )

        if intent in (
            "open",
            "close",
            "search",
            "youtube",
        ):
            return Decision(
                route="TOOL",
                intent=intent,
            )

        if intent in (
            "add_goal",
            "next_task",
            "show_goals",
            "goal_progress",
        ):
            return Decision(
                route="PLANNER",
                intent=intent,
            )

        return Decision(
            route="AI",
            intent=intent,
        )