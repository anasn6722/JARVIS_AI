class ReferenceResolver:

    def __init__(self, memory):
        self.memory = memory

    def resolve(self, command):

        text = command.original.lower()

        #
        # Close it
        #
        if (
            command.intent == "close"
            and "it" in text
        ):

            app = self.memory.get_last_app()

            if app:
                command.entities["apps"] = [app]

            website = self.memory.get_last_website()

            if website:
                command.entities["websites"] = [website]

        #
        # Open it
        #
        elif (
            command.intent == "open"
            and "it" in text
        ):

            app = self.memory.get_last_app()

            if app:
                command.entities["apps"] = [app]

        return command