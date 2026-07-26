class IntentRecognizer:

    def recognize(self, command: str):
        command = command.lower().strip()

        # Specific phrases first
        if command == "last message":
            return "last_message"

        if command == "who are you":
            return "identity"

        if command.startswith("search "):
            return "search"

        if command.startswith("youtube "):
            return "youtube"

        if any(
            word in command
            for word in (
                "open",
                "launch",
                "start",
            )
        ):
            return "open"

        if command == "time" or "what is the time" in command:
            return "time"

        if command in ("hello", "hi", "hey"):
            return "hello"

        if command == "show history":
            return "history"

        if command.startswith("my name is "):
            return "set_name"

        if command == "what is my name":
            return "get_name"

        return "unknown"