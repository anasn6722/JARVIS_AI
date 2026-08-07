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

    def run(self, graph):

        print("=" * 60)
        print("GRAPH RUNNER START")
        print("=" * 60)
    
        print("Nodes in graph:")
    
        for node in graph.all_nodes():
            print(
                node.id,
                node.task.action,
                node.task.target,
            )
    
        context = WorkflowContext([])
    
        context.status = WorkflowStatus.RUNNING
    
        while True:
        
            ready = self.ready_nodes(graph)
    
            print("READY:", len(ready))
    
            if not ready:
                break
            
            for node in ready:
            
                print(
                    "Executing:",
                    node.task.action,
                    node.task.target,
                )
    
                self.execute_node(node)
    
        print("=" * 60)
        print("GRAPH RUNNER FINISHED")
        print("=" * 60)
    
        responses = []
    
        for node in graph.all_nodes():
        
            if node.task.success and node.task.result:
            
                responses.append(node.task.result)
    
        return "\n".join(responses)
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