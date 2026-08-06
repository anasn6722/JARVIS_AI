class ResponseStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        if not context.response:
            return

        self.brain.chat_memory.add(
            "Assistant",
            context.response,
        )

        self.brain.conversation_manager.remember_response(
            context.response
        )