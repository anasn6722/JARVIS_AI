class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        self.brain.execution_manager.execute(context)

        context.stop = True