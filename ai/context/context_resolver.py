class ContextResolver:

    def __init__(self, conversation_memory):
        self.memory = conversation_memory

    def resolve(self, command):

        entities = command.entities

        # -------------------------
        # Pronouns
        # -------------------------

        pronouns = {
            "it",
            "that",
            "there",
            "this",
            "previous",
            "last",
        }

        if entities.apps:
            return

        if entities.websites:
            return

        words = command.original.lower().split()

        if not any(word in pronouns for word in words):
            return

        # last application

        app = self.memory.last_app()

        if app:
            entities.apps.append(app)
            return

        # last website

        website = self.memory.last_website()

        if website:
            entities.websites.append(website)