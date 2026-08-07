class BuiltinExecutor:

    def __init__(
        self,
        builtin_handler,
    ):
        self.builtin_handler = builtin_handler

    def execute(
        self,
        context,
    ):
        return self.builtin_handler.execute(
            context.decision.intent,
            context.command.original,
        )