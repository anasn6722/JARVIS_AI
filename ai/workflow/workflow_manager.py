from ai.workflow.linear_runner import LinearRunner


class WorkflowManager:


    def __init__(
        self,
        tool_executor,
    ):

        self.linear_runner = LinearRunner(
            tool_executor
        )


    def run(
        self,
        tasks,
    ):

        return self.linear_runner.run(tasks)



    def run_action(
        self,
        action,
        target,
    ):

        from ai.agent.task import Task


        task = Task(
            action=action,
            target=target,
        )


        return self.run(
            [task]
        )