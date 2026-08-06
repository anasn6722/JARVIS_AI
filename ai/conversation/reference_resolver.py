class ReferenceResolver:

    def __init__(self, memory):
        self.memory = memory

    def resolve(self, command):

        text = command.original.lower()

        pronouns = {
            "it",
            "that",
            "there",
            "last",
            "previous",
        }

        has_reference = any(
            word in text.split()
            for word in pronouns
        )

        if not has_reference:
            return command

        app = self.memory.last_app()
        website = self.memory.last_website()
        search = self.memory.last_search()

        # -------------------------
        # OPEN
        # -------------------------

        if (
            command.intent == "open"
            and app
            and not command.entities["apps"]
        ):
            command.entities["apps"] = [app]

        elif (
            command.intent == "open"
            and website
            and not command.entities["websites"]
        ):
            command.entities["websites"] = [website]

        # -------------------------
        # CLOSE
        # -------------------------

        if (
            command.intent == "close"
            and app
            and not command.entities["apps"]
        ):
            command.entities["apps"] = [app]

        elif (
            command.intent == "close"
            and website
            and not command.entities["websites"]
        ):
            command.entities["websites"] = [website]

        # -------------------------
        # SEARCH
        # -------------------------

        if (
            command.intent == "search"
            and search
            and not command.entities["searches"]
        ):
            command.entities["searches"] = [search]

        return command