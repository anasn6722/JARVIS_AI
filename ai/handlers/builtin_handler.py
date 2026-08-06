from datetime import datetime, timezone


class BuiltinHandler:

    def __init__(self, brain):
        self.brain = brain


    def hello(self):
        return "Hello Anas! 👋"


    def identity(self):
        return (
            "I am JARVIS, "
            "your personal AI assistant."
        )


    def time(self):

        return datetime.now(
            timezone.utc
        ).astimezone().strftime(
            "Current time: %I:%M:%S %p"
        )