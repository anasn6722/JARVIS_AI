class ExecutionEngine:

    def __init__(
        self,
        workflow_manager,
    ):
        self.workflow_manager = workflow_manager

    def execute(
        self,
        tasks,
        graph=None,
    ):
        return self.workflow_manager.run(
            tasks=tasks,
            graph=graph,
        )