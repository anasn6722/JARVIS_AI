class PluginExecutor:

    def __init__(
        self,
        execution_handler,
    ):
        self.execution_handler = execution_handler

    def execute(
        self,
        context,
    ):
        return self.execution_handler.plugin(
            context.decision.intent,
            context.command.original,
        )