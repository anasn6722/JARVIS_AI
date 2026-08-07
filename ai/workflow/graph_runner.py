from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_event import WorkflowEvent
from ai.workflow.workflow_status import WorkflowStatus


class GraphRunner:

    def __init__(
        self,
        tool_executor,
        events,
        retry_manager,
    ):
        self.tool_executor = tool_executor
        self.events = events
        self.retry_manager = retry_manager

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

                success = self.execute_node(node)

                if success:

                    context.completed.append(
                        node.task
                    )

                else:

                    context.failed.append(
                        node.task
                    )

                    context.result.errors.append(
                        node.task.error
                    )

        if context.failed:

            context.status = WorkflowStatus.FAILED

        else:

            context.status = WorkflowStatus.COMPLETED

        self.events.publish(
            WorkflowEvent(
                name="GRAPH_FINISHED",
                data=context,
            )
        )

        return self.build_result(context)

    def ready_nodes(
        self,
        graph,
    ):

        ready = []

        for node in graph.all_nodes():

            if node.completed:
                continue

            if getattr(node, "running", False):
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

    def build_result(
        self,
        context,
    ):

        responses = []

        for task in context.completed:

            if task.result:

                responses.append(
                    task.result
                )

        for task in context.failed:

            responses.append(
                f"Failed: {task.action}"
            )

        context.result.success = (
            len(context.failed) == 0
        )

        context.result.completed_tasks = len(
            context.completed
        )

        context.result.failed_tasks = len(
            context.failed
        )

        context.result.response = "\n".join(
            responses
        )

        return context.result.response