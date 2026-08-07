from ai.workflow.event_bus import EventBus
from ai.workflow.retry_manager import RetryManager
from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_event import WorkflowEvent
from ai.workflow.workflow_status import WorkflowStatus


class GraphRunner:

    def __init__(
        self,
        tool_executor,
    ):

        self.tool_executor = tool_executor
        self.events = EventBus()
        self.retry_manager = RetryManager()

    def run(
        self,
        graph,
    ):

        context = WorkflowContext([])

        context.status = WorkflowStatus.RUNNING

        self.events.publish(
            WorkflowEvent(
                name="GRAPH_STARTED",
                data=context,
            )
        )

        while True:

            ready = self.ready_nodes(graph)

            if not ready:
                break

            for node in ready:

                self.execute_node(node)

        context.status = WorkflowStatus.COMPLETED

        self.events.publish(
            WorkflowEvent(
                name="GRAPH_FINISHED",
                data=context,
            )
        )

        return context

    def root_nodes(self, graph):
        return [
            node
            for node in graph.all_nodes()
            if not node.parents
        ]


    def ready_nodes(self, graph):

        ready = []

        for node in graph.all_nodes():

            if node.completed:
                continue

            if node.running:
                continue

            parents_complete = True

            for parent_id in node.parents:

                parent = graph.get(parent_id)

                if not parent.completed:

                    parents_complete = False
                    break

            if parents_complete:

                ready.append(node)

        return ready

    def execute_node(
        self,
        node,
    ):

        node.running = True

        try:

            result = self.tool_executor.execute(
                node.task.action,
                node.task.target,
            )

            node.task.result = result
            node.task.success = True
            node.task.completed = True

            node.completed = True
            node.running = False

            return True

        except Exception as e:

            node.task.error = str(e)
            node.task.success = False

            node.running = False
            node.failed = True

            return False


    def execute_ready_nodes(
        self,
        graph,
    ):

        ready = self.ready_nodes(graph)

        for node in ready:

            self.execute_node(node)