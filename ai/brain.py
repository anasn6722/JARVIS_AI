from datetime import datetime, timezone


class Brain:
    """
    The central command processor for JARVIS.
    """

    def process(self, command: str) -> str:
        """
        Process a user command and return a response.
        """

        command = command.lower().strip()

        if command == "hello":
            return "Hello Anas! 👋"

        if command == "who are you":
            return "I am JARVIS, your personal AI assistant."

        if command == "time":
            return datetime.now(timezone.utc).astimezone().strftime(
            "Current time: %I:%M:%S %p"
            )
            

        return "Sorry, I don't understand that command yet."