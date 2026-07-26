class IntentRecognizer:
    def recognize(self, command: str):
        command = command.lower().strip()

        if command.startswith("open "):
            return "open"

        if command.startswith("search "):
            return "search"

        if command.startswith("youtube "):
            return "youtube"

        if command == "time":
            return "time"

        if command == "hello":
            return "hello"

        if command == "who are you":
            return "identity"

        return "unknown"