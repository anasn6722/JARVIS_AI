class PluginExecutor:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, context):

        return self.brain.execution_handler.plugin(
            context.decision.intent,
            context.command.original,
        )