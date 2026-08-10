from ai.memory.execution.execution_memory import ExecutionMemory
from ai.workflow.event_bus import EventBus
from ai.workflow.graph_runner import GraphRunner
from ai.workflow.linear_runner import LinearRunner
from ai.workflow.retry_manager import RetryManager
from ai.workflow.scheduler import Scheduler


class WorkflowManager:

    def __init__(
        self,
        tool_executor,
        execution_memory=None,

    ):

        self.tool_executor = tool_executor
        self.execution_memory = (
            execution_memory
            or ExecutionMemory()
        )

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
            self.execution_memory,
        )

    def run(
        self,
        tasks=None,
        graph=None,
        goal_id=None,
    ):
        if graph is not None:
            print(">>> USING GRAPH RUNNER")
            return self.graph_runner.run(
                graph,
                goal_id=goal_id,
            )
    
        print(">>> USING LINEAR RUNNER")
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
            tasks=[task],
        )