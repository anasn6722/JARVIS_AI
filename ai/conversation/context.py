class Context:
    """Shared conversation state used by JARVIS."""

    def __init__(self):
        # =========================================================
        # CONVERSATION
        # =========================================================

        self.last_response = None

        # =========================================================
        # GOALS
        # =========================================================

        self.current_goal = None
        self.current_task = None
        self.current_lesson = None

        # =========================================================
        # OPENED / REFERENCED THINGS
        # =========================================================

        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None

        # =========================================================
        # LAST REFERENCE
        # =========================================================
        #
        # Examples:
        #
        # ("app", "chrome")
        # ("website", "youtube")
        # ("search", "python tutorials")
        #
        # Used by ConversationMemory and ReferenceResolver.
        # =========================================================

        self.last_reference = None

    def clear(self):
        """Reset all conversation context."""

        self.last_response = None

        self.current_goal = None
        self.current_task = None
        self.current_lesson = None

        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None

        self.last_reference = None