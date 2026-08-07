from ai.workflow.event_bus import EventBus
from ai.workflow.graph_runner import GraphRunner
from ai.workflow.linear_runner import LinearRunner
from ai.workflow.retry_manager import RetryManager
from ai.workflow.scheduler import Scheduler


class WorkflowManager:

    def __init__(
        self,
        tool_executor,
    ):

        self.tool_executor = tool_executor

        self.events = EventBus()
        self.retry_manager = RetryManager()
        self.scheduler = Scheduler(self)

        self.linear_runner = LinearRunner(
            tool_executor,
        )

        self.graph_runner = GraphRunner(
            tool_executor,
            self.events,
            self.retry_manager,
        )

    def run(
        self,
        tasks=None,
        graph=None,
    ):

        if graph is not None:

            return self.graph_runner.run(
                graph,
            )

        return self.linear_runner.run(
            tasks,
        )

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
            tasks=[task],
        )