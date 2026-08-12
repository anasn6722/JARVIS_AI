
from datetime import datetime

from ai.memory.execution.execution_record import ExecutionRecord
from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_status import WorkflowStatus


class GraphRunner:
    """Execute tasks according to their graph dependencies."""

    def __init__(
        self,
        tool_executor,
        events,
        retry_manager,
        execution_memory=None,
    ):
        self.tool_executor = tool_executor
        self.events = events
        self.retry_manager = retry_manager
        self.execution_memory = execution_memory

    # ============================================================
    # RUN GRAPH
    # ============================================================

    def run(
        self,
        graph,
        goal_id=None,
    ):
        print("=" * 60)
        print("GRAPH RUNNER START")
        print("=" * 60)

        print("Nodes in graph:")

        for node in graph.nodes.values():
            print(
                node.task.action,
                node.task.target,
            )

        context = WorkflowContext([])
        context.status = WorkflowStatus.RUNNING

        # ========================================================
        # GRAPH EXECUTION LOOP
        # ========================================================

        while not graph.completed():

            ready = graph.executable()

            print(
                "READY:",
                len(ready),
            )

            if not ready:
                print(
                    "No executable nodes remaining."
                )
                break

            for node in ready:

                print(
                    "Executing:",
                    node.task.action,
                    node.task.target,
                )

                self.execute_node(
                    node,
                    goal_id=goal_id,
                )

        # ========================================================
        # CHECK FAILED NODES
        # ========================================================

        failed_nodes = [
            node
            for node in graph.nodes.values()
            if node.failed
        ]

        if failed_nodes:

            context.status = WorkflowStatus.FAILED

            print("=" * 60)
            print("GRAPH RUNNER FAILED")
            print("=" * 60)

            return self.build_graph_result(graph)

        # ========================================================
        # CHECK WHETHER GRAPH ACTUALLY COMPLETED
        # ========================================================

        if not graph.completed():

            context.status = WorkflowStatus.FAILED

            print("=" * 60)
            print("GRAPH RUNNER FAILED")
            print("=" * 60)

            return self.build_graph_result(graph)

        # ========================================================
        # SUCCESS
        # ========================================================

        context.status = WorkflowStatus.COMPLETED

        print("=" * 60)
        print("GRAPH RUNNER FINISHED")
        print("=" * 60)

        return self.build_graph_result(graph)

    # ============================================================
    # EXECUTE NODE
    # ============================================================

        
    def execute_node(
        self,
        node,
        goal_id=None,
    ):
        """Execute one ready graph node."""
    
        if (
            node.completed
            or node.failed
            or node.blocked
        ):
            return False
    
        if not node.ready:
            return False
    
        started = datetime.now()
    
        try:
            print(
                "Tool:",
                node.task.action,
                node.task.target,
            )
    
            # ====================================================
            # EXECUTE TOOL
            # ====================================================
    
            if node.task.target:
                result = self.tool_executor.execute(
                    node.task.action,
                    node.task.target,
                )
            else:
                result = self.tool_executor.execute(
                    node.task.action,
                )
    
            completed = datetime.now()
    
            # ====================================================
            # SAVE EXECUTION HISTORY
            # ====================================================
    
            if self.execution_memory is not None:
                self.execution_memory.add(
                    ExecutionRecord(
                        goal_id=goal_id or "",
                        action=node.task.action,
                        target=node.task.target,
                        success=True,
                        result=str(result),
                        started=started,
                        completed=completed,
                    )
                )
    
            # ====================================================
            # SUCCESS
            # ====================================================
    
            node.task.result = result
            node.task.success = True
            node.task.error = ""
            node.task.completed = True
    
            node.completed = True
            node.failed = False
    
            return True
    
        except Exception as error:
            completed = datetime.now()
    
            # ====================================================
            # FAILURE
            # ====================================================
    
            node.task.error = str(error)
            node.task.success = False
            node.task.completed = False
    
            node.failed = True
    
            # ====================================================
            # SAVE FAILED EXECUTION
            # ====================================================
    
            if self.execution_memory is not None:
                self.execution_memory.add(
                    ExecutionRecord(
                        goal_id=goal_id or "",
                        action=node.task.action,
                        target=node.task.target,
                        success=False,
                        result="",
                        error=str(error),
                        started=started,
                        completed=completed,
                    )
                )
    
            print(
                "GRAPH NODE FAILED:",
                node.task.action,
                node.task.target,
            )
    
            print(
                "ERROR:",
                error,
            )
    
            return False
    
    
    # ============================================================
    # BUILD GRAPH RESULT
    # ============================================================

    def build_graph_result(
        self,
        graph,
    ):
        """Build a readable response from graph task results."""

        responses = []

        for node in graph.nodes.values():

            task = node.task

            if task.result is not None:

                result = task.result

                if isinstance(result, tuple):

                    success, message = result

                    responses.append(
                        str(message)
                    )

                else:

                    responses.append(
                        str(result)
                    )

            elif node.failed:

                responses.append(
                    f"Failed: {task.action}: "
                    f"{task.error}"
                )

        if not responses:
            return "No results were produced."

        return "\n".join(responses)
