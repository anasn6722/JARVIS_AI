class MemoryHandler:

    def __init__(self, brain):
        self.brain = brain

    # -----------------------------
    # Conversation History
    # -----------------------------

    def last_message(self):

        history = self.brain.chat_memory.get_all()

        if len(history) >= 2:
            return (
                f"Your last message was: "
                f"{history[-2]['message']}"
            )

        return "I don't remember any previous message."

    def history(self):

        history = self.brain.chat_memory.get_all()

        if len(history) <= 1:
            return "No previous conversation found."

        response = "Conversation History:\n\n"

        for i, item in enumerate(
            history[:-1],
            start=1,
        ):

            response += (
                f"{i}. "
                f"{item['speaker']}: "
                f"{item['message']}\n"
            )

        return response

    # -----------------------------
    # Profile
    # -----------------------------

    def set_name(self, command):

        name = command.replace(
            "my name is",
            "",
            1,
        ).strip()

        if not name:
            return "Please tell me your name."

        self.brain.memory_manager.profile.set(
            "name",
            name,
        )

        return f"Nice to meet you, {name}!"

    def get_name(self):

        name = self.brain.memory_manager.profile.get(
            "name"
        )

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."

    # -----------------------------
    # Preferences
    # -----------------------------

    def set_preference(self, command):

        key, value = (
            self.brain.memory_extractor.extract(
                command
            )
        )

        if not key:
            return "I couldn't understand."

        self.brain.memory.remember(
            key,
            value,
        )

        return (
            f"I'll remember that your "
            f"{key.replace('_',' ')} "
            f"is {value}."
        )

    def get_preference(self, command):

        key = (
            self.brain.memory_query_parser.extract(
                command
            )
        )

        if not key:
            return (
                "I don't know what "
                "you're asking."
            )

        value = self.brain.memory.recall(
            key
        )

        if value:
            return (
                f"Your "
                f"{key.replace('_',' ')} "
                f"is {value}."
            )

        return (
            f"I don't know your "
            f"{key.replace('_',' ')} "
            f"yet."
        )