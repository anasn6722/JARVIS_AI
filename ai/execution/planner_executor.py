class PlannerExecutor:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, context):

        return self.brain.execution_engine.execute(
            context.tasks
        )