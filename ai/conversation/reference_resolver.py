class ReferenceResolver:
    """Resolves pronouns such as 'it', 'that', and 'last'."""

    def __init__(self, memory):
        self.memory = memory

    # ============================================================
    # RESOLVE REFERENCE
    # ============================================================

    def resolve(self, command):
        """Resolve references using the most recent memory."""

        text = command.original.lower()

        # --------------------------------------------------------
        # Pronouns / Reference Words
        # --------------------------------------------------------

        pronouns = {
            "it",
            "that",
            "there",
            "last",
            "previous",
        }

        words = text.split()

        has_reference = any(
            word in words
            for word in pronouns
        )

        if not has_reference:
            return command

        # ========================================================
        # GET LAST KNOWN REFERENCES
        # ========================================================

        app = self.memory.last_app()
        website = self.memory.last_website()
        search = self.memory.last_search()

        # --------------------------------------------------------
        # Most recent reference
        # --------------------------------------------------------

        reference = None

        if hasattr(self.memory, "last_reference"):
            reference = self.memory.last_reference()

        # ========================================================
        # DEBUG
        # ========================================================

        print("=" * 50)
        print("REFERENCE RESOLVER")
        print(f"Input: {command.original}")
        print(f"Reference: {reference}")
        print(f"App: {app}")
        print(f"Website: {website}")
        print(f"Search: {search}")

        # ========================================================
        # OPEN
        # ========================================================

        if command.intent == "open":

            # ----------------------------------------------------
            # Most recent reference has priority
            # ----------------------------------------------------

            if reference:

                reference_type, reference_value = reference

                if reference_type == "app":

                    command.entities["apps"] = [
                        reference_value
                    ]

                    command.entities["websites"] = []

                elif reference_type == "website":

                    command.entities["websites"] = [
                        reference_value
                    ]

                    command.entities["apps"] = []

            # ----------------------------------------------------
            # Fallback: website
            # ----------------------------------------------------

            elif website:

                command.entities["websites"] = [
                    website
                ]

                command.entities["apps"] = []

            # ----------------------------------------------------
            # Fallback: application
            # ----------------------------------------------------

            elif app:

                command.entities["apps"] = [
                    app
                ]

                command.entities["websites"] = []

        # ========================================================
        # CLOSE
        # ========================================================

        elif command.intent == "close":

            # ----------------------------------------------------
            # Most recent reference has priority
            #
            # Example:
            #
            # open chrome
            # open youtube
            # close it
            #
            # "it" should refer to youtube.
            # ----------------------------------------------------

            if reference:

                reference_type, reference_value = reference

                if reference_type == "app":

                    command.entities["apps"] = [
                        reference_value
                    ]

                    command.entities["websites"] = []

                elif reference_type == "website":

                    command.entities["websites"] = [
                        reference_value
                    ]

                    command.entities["apps"] = []

            # ----------------------------------------------------
            # Fallback: application
            # ----------------------------------------------------

            elif app:

                command.entities["apps"] = [
                    app
                ]

                command.entities["websites"] = []

            # ----------------------------------------------------
            # Fallback: website
            # ----------------------------------------------------

            elif website:

                command.entities["websites"] = [
                    website
                ]

                command.entities["apps"] = []

        # ========================================================
        # SEARCH
        # ========================================================

        elif command.intent == "search":

            if search:

                command.entities["searches"] = [
                    search
                ]

        # ========================================================
        # DEBUG RESULT
        # ========================================================

        print(
            f"Resolved apps: "
            f"{command.entities.get('apps', [])}"
        )

        print(
            f"Resolved websites: "
            f"{command.entities.get('websites', [])}"
        )

        print("=" * 50)

        # ========================================================
        # RETURN
        # ========================================================

        return command