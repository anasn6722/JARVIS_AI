class GoalClassifier:

    def classify(self, command: str):
        command = command.lower()

        if any(word in command for word in [
            "learn",
            "study",
            "tutorial",
        ]):
            return "learn"

        if any(word in command for word in [
            "buy",
            "purchase",
            "order",
        ]):
            return "shopping"

        if any(word in command for word in [
            "news",
            "latest",
        ]):
            return "news"

        return "general"