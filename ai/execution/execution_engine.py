class ExecutionEngine:

    def __init__(self, brain):

        self.brain = brain

    def execute(self, tasks):

        return self.brain.workflow_manager.run(
            tasks
        )