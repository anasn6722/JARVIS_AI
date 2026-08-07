class PlannerExecutor:

    def __init__(
        self,
        execution_engine,
    ):
        self.execution_engine = execution_engine

    def execute(
        self,
        context,
    ):
        return self.execution_engine.execute(
            tasks=context.tasks,
            graph=context.graph,
        )