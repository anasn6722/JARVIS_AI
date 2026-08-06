from typing import ClassVar


class GoalClassifier:

    GOAL_KEYWORDS: ClassVar[set[str]] = {
        "build",
        "create",
        "make",
        "develop",
        "design",

        "learn",
        "study",
        "master",

        "plan",
        "organize",
        "prepare",

        "buy",
        "purchase",
        "order",

        "write",
        "generate",

        "improve",
        "upgrade",
        "fix",

        "start",
    }

    NON_GOALS: ClassVar[set[str]] = {
        "open",
        "close",
        "search",
        "find",

        "time",
        "date",

        "hello",
        "hi",
    }

    def classify(self, command: str):

        words = command.lower().split()

        # Ignore simple commands
        for word in self.NON_GOALS:
            if words and words[0] == word:
                return {
                    "type": "project",
                    "goal": command,
                }

        # Detect long-term goals
        for word in words:
            if word in self.GOAL_KEYWORDS:
                return "goal"

        return None