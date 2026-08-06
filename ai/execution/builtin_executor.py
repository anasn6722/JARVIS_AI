class BuiltinExecutor:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, context):

        return self.brain.builtin.execute(
            context.decision.intent,
            context.command.original,
        )