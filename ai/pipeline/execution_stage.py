class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        # AI commands are handled by AIStage.
        if context.decision and context.decision.route == "AI":
            return

        self.brain.execution_manager.execute(context)

        context.stop = True