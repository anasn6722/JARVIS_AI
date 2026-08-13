class ResponseStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        if not context.response:
            if context.verification_errors:
                context.response = (
                    "I couldn't complete the request."
                )
            else:
                context.response = (
                    "The request completed, "
                    "but no response was produced."
                )

        if context.verification_errors:
            errors = "\n".join(
                f"- {error}"
                for error in context.verification_errors
            )

            context.response = (
                "I couldn't complete the request.\n"
                f"{errors}"
            )

        self.brain.chat_memory.add(
            "Assistant",
            context.response,
        )

        self.brain.conversation_manager.remember_response(
            context.response
        )

        context.stop = True