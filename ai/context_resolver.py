class ContextResolver:

    def __init__(self, context):
        self.context = context

    def resolve(self, command):

        command = command.lower()

        # -------------------------
        # Goal references
        # -------------------------

        if (
            any(word in command for word in ("it", "my goal", "that goal"))
            and self.context.current_goal
        ):
            command = command.replace(
                "it",
                self.context.current_goal,
            )

        # -------------------------
        # Search references
        # -------------------------

        if "search it" in command and self.context.last_search:
            command = command.replace(
                "it",
                self.context.last_search,
            )

        # -------------------------
        # Open App
        # -------------------------

        if "open it" in command and self.context.last_app:
            command = command.replace(
                "it",
                self.context.last_app,
            )

        # -------------------------
        # Close App ⭐ NEW
        # -------------------------

        if "close it" in command and self.context.last_app:
            command = command.replace(
                "it",
                self.context.last_app,
            )

        # -------------------------
        # Website
        # -------------------------

        if (
            "open that website" in command
            and self.context.last_website
        ):
            command = command.replace(
                "that website",
                self.context.last_website,
            )

        # -------------------------
        # Video ⭐ NEW
        # -------------------------

        if (
            "play it" in command
            and self.context.last_search
        ):
            command = command.replace(
                "it",
                self.context.last_search,
            )

        return command