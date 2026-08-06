from datetime import datetime, timezone

from ai.command_parser import CommandParser


class ChatHandler:

    def __init__(self, brain):
        self.brain = brain

    # ------------------------------------
    # Greetings
    # ------------------------------------

    def hello(self):

        name = self.brain.profile.get("name")

        if name:
            return f"Hello {name}! 👋"

        return "Hello! 👋"

    # ------------------------------------
    # Identity
    # ------------------------------------

    def identity(self):

        return (
            "I am JARVIS, "
            "your personal AI assistant."
        )

    # ------------------------------------
    # Time
    # ------------------------------------

    def time(self):

        return datetime.now(
            timezone.utc
        ).astimezone().strftime(
            "Current time: %I:%M:%S %p"
        )

    # ------------------------------------
    # Google Search
    # ------------------------------------

    def search(self, command):

        query = CommandParser.search_query(
            command
        )

        self.brain.context.update(
            search=query,
        )

        self.brain.web.google_search(
            query
        )

        return (
            f"Searching Google for "
            f"{query}."
        )

    # ------------------------------------
    # YouTube Search
    # ------------------------------------

    def youtube(self, command):

        query = CommandParser.youtube_query(
            command
        )

        self.brain.web.youtube_search(
            query
        )

        return (
            f"Searching YouTube for "
            f"{query}."
        )