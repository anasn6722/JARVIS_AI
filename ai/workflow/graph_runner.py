
from ai.workflow.workflow_context import WorkflowContext
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

    # ============================================================
    # RUN GRAPH
    # ============================================================

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

        # ========================================================
        # GRAPH EXECUTION LOOP
        # ========================================================

        while True:

            ready = self.ready_nodes(graph)

            print(
                "READY:",
                len(ready),
            )

            if not ready:
                break

            # ----------------------------------------------------
            # Execute every currently ready node
            # ----------------------------------------------------

            for node in ready:

                print(
                    "Executing:",
                    node.task.action,
                    node.task.target,
                )

                self.execute_node(node)

        # ========================================================
        # FINISHED
        # ========================================================

        context.status = WorkflowStatus.COMPLETED

        print("=" * 60)
        print("GRAPH RUNNER FINISHED")
        print("=" * 60)

        # ========================================================
        # BUILD RESPONSE
        # ========================================================

        responses = []

        for node in graph.all_nodes():

            if (
                node.task.success
                and node.task.result
            ):
                responses.append(
                    node.task.result
                )

        formatted_responses = []

        for response in responses:
        
            if isinstance(response, tuple):
                success, message = response

                if success:
                    formatted_responses.append(
                        str(message)
                    )
                else:
                    formatted_responses.append(
                        str(message)
                    )

            else:
                formatted_responses.append(
                    str(response)
                )

        return "\n".join(formatted_responses)

    # ============================================================
    # FIND READY NODES
    # ============================================================

    def ready_nodes(
        self,
        graph,
    ):

        ready = []

        for node in graph.all_nodes():

            # ----------------------------------------------------
            # IMPORTANT:
            #
            # Use BOTH task.completed and node.completed.
            #
            # This prevents a task from being executed again
            # if either layer has already marked it completed.
            # ----------------------------------------------------

            if (
                node.completed
                or node.task.completed
            ):
                continue

            # ----------------------------------------------------
            # Already running
            # ----------------------------------------------------

            if getattr(
                node,
                "running",
                False,
            ):
                continue

            # ----------------------------------------------------
            # Failed nodes are not automatically executed again
            # by the graph runner.
            # ----------------------------------------------------

            if getattr(
                node,
                "failed",
                False,
            ):
                continue

            # ----------------------------------------------------
            # Check parent dependencies
            # ----------------------------------------------------

            parents_complete = True

            for parent_id in node.parents:

                parent = graph.get(parent_id)

                if parent is None:
                    parents_complete = False
                    break

                if not (
                    parent.completed
                    or parent.task.completed
                ):
                    parents_complete = False
                    break

            if parents_complete:

                ready.append(node)

        return ready

    # ============================================================
    # EXECUTE NODE
    # ============================================================

    def execute_node(
        self,
        node,
    ):
    
        # --------------------------------------------------------
        # Safety check
        # --------------------------------------------------------
    
        if (
            node.completed
            or node.task.completed
        ):
            return True
    
        node.running = True
    
        try:
        
            print(
                "Tool:",
                node.task.action,
                node.task.target,
            )
    
            # ====================================================
            # EXECUTE TOOL
            # ====================================================
            #
            # Some tools require an argument:
            #
            #     focus_window("VS Code")
            #     close_window("Chrome")
            #
            # Other tools require no argument:
            #
            #     active_window()
            #     list_windows()
            #
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
    
            # ====================================================
            # SUCCESS
            # ====================================================
    
            node.task.result = result
    
            node.task.success = True
    
            node.task.error = ""
    
            node.task.completed = True
    
            node.completed = True
    
            node.failed = False
    
            node.running = False
    
            return True
    
        except Exception as e:
        
            # ====================================================
            # FAILURE
            # ====================================================
    
            node.task.error = str(e)
    
            node.task.success = False
    
            node.task.completed = False
    
            node.failed = True
    
            node.running = False
    
            print(
                "GRAPH NODE FAILED:",
                node.task.action,
                node.task.target,
            )
    
            print(
                "ERROR:",
                e,
            )
    
            return False
    # ============================================================
    # BUILD RESULT
    # ============================================================

    def build_result(
        self,
        context,
    ):

        responses = []

        # --------------------------------------------------------
        # Completed tasks
        # --------------------------------------------------------

        for task in context.completed:

            if task.result:

                responses.append(
                    task.result
                )

        # --------------------------------------------------------
        # Failed tasks
        # --------------------------------------------------------

        for task in context.failed:

            responses.append(
                f"Failed: {task.action}"
            )

        # --------------------------------------------------------
        # Result information
        # --------------------------------------------------------

        context.result.success = (
            len(context.failed) == 0
        )

        context.result.completed_tasks = (
            len(context.completed)
        )

        context.result.failed_tasks = (
            len(context.failed)
        )

        context.result.response = (
            "\n".join(responses)
        )

        return context.result.response
