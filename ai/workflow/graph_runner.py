from datetime import datetime

from ai.memory.execution.execution_record import ExecutionRecord
from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_event import WorkflowEvent
from ai.workflow.workflow_status import WorkflowStatus
from desktop_automation.planner.task_context import TaskContext


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

        # Context shared by tasks during one graph execution.
        self.task_context = TaskContext()

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

        # Start every graph with a clean task context.
        self.task_context.clear()

        context = WorkflowContext(
            [
                node.task
                for node in graph.nodes.values()
            ]
        )

        context.status = WorkflowStatus.RUNNING

        # ========================================================
        # WORKFLOW START EVENT
        # ========================================================

        self.events.publish(
            WorkflowEvent(
                name="WORKFLOW_STARTED",
                data=context,
            )
        )

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

                self.events.publish(
                    WorkflowEvent(
                        name="TASK_STARTED",
                        task=node.task,
                        data=context,
                    )
                )

                self.execute_node(
                    node,
                    goal_id=goal_id,
                )

                if node.completed:

                    context.completed.append(
                        node.task
                    )

                    self.events.publish(
                        WorkflowEvent(
                            name="TASK_COMPLETED",
                            task=node.task,
                            data=context,
                        )
                    )

                elif node.failed:

                    context.failed.append(
                        node.task
                    )

                    context.result.errors.append(
                        node.task.error
                    )

                    self.events.publish(
                        WorkflowEvent(
                            name="TASK_FAILED",
                            task=node.task,
                            data=context,
                        )
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

            self.events.publish(
                WorkflowEvent(
                    name="WORKFLOW_FINISHED",
                    data=context,
                )
            )

            return self.build_graph_result(
                graph
            )

        # ========================================================
        # CHECK WHETHER GRAPH ACTUALLY COMPLETED
        # ========================================================

        if not graph.completed():

            context.status = WorkflowStatus.FAILED

            print("=" * 60)
            print("GRAPH RUNNER FAILED")
            print("=" * 60)

            self.events.publish(
                WorkflowEvent(
                    name="WORKFLOW_FINISHED",
                    data=context,
                )
            )

            return self.build_graph_result(
                graph
            )

        # ========================================================
        # SUCCESS
        # ========================================================

        context.status = WorkflowStatus.COMPLETED

        print("=" * 60)
        print("GRAPH RUNNER FINISHED")
        print("=" * 60)

        self.events.publish(
            WorkflowEvent(
                name="WORKFLOW_FINISHED",
                data=context,
            )
        )

        return self.build_graph_result(
            graph
        )

    # ============================================================
    # EXECUTE NODE
    # ============================================================

    def execute_node(
        self,
        node,
        goal_id=None,
    ):
        """Execute one ready graph node with retry support."""

        if (
            node.completed
            or node.failed
            or node.blocked
        ):
            return False

        if not node.ready:
            return False

        node.running = True

        started = datetime.now()

        while True:

            try:
                print(
                    "Tool:",
                    node.task.action,
                    node.task.target,
                )

                # =================================================
                # RESOLVE TARGET
                # =================================================

                resolved_target = (
                    self._resolve_target(
                        node.task.target
                    )
                )

                print(
                    "Resolved target:",
                    resolved_target,
                )

                # =================================================
                # EXECUTE TOOL
                # =================================================

                if resolved_target is not None:

                    raw_result = (
                        self.tool_executor.execute(
                            node.task.action,
                            resolved_target,
                        )
                    )

                else:

                    raw_result = (
                        self.tool_executor.execute(
                            node.task.action
                        )
                    )

                completed = datetime.now()

                # =================================================
                # NORMALIZE RESULT
                # =================================================

                if (
                    isinstance(
                        raw_result,
                        tuple,
                    )
                    and len(raw_result) == 2
                    and isinstance(
                        raw_result[0],
                        bool,
                    )
                ):

                    success, message = raw_result

                    node.task.success = success

                    node.task.result = message

                else:

                    success = True

                    node.task.success = True
                    node.task.result = raw_result

                # =================================================
                # SUCCESS
                # =================================================

                if success:

                    node.task.success = True
                    node.task.error = ""
                    node.task.completed = True

                    node.completed = True
                    node.failed = False
                    node.running = False

                    print(
                        "Success:",
                        True,
                    )

                    print(
                        "Result:",
                        node.task.result,
                    )

                    # =============================================
                    # TASK CONTEXT
                    # =============================================

                    self.task_context.set(
                        "last_result",
                        node.task.result,
                    )

                    self.task_context.set(
                        "last_action",
                        node.task.action,
                    )

                    self.task_context.set(
                        "last_target",
                        node.task.target,
                    )

                    self.task_context.set(
                        f"task:{node.task.id}",
                        node.task.result,
                    )

                    self.task_context.set(
                        f"result:{node.task.action}",
                        node.task.result,
                    )

                    # =============================================
                    # LAST UI DESCRIPTOR
                    # =============================================

                    if (
                        node.task.action
                        in {
                            "ui_find_descriptor",
                            "ui_describe",
                        }
                        and isinstance(
                            node.task.result,
                            dict,
                        )
                    ):

                        self.task_context.set(
                            "last_ui",
                            node.task.result,
                        )

                        print(
                            "LAST UI:",
                            node.task.result,
                        )

                    print(
                        "TASK CONTEXT:",
                        self.task_context.snapshot(),
                    )

                    # =============================================
                    # EXECUTION MEMORY
                    # =============================================

                    if (
                        self.execution_memory
                        is not None
                    ):

                        self.execution_memory.add(
                            ExecutionRecord(
                                goal_id=goal_id or "",
                                action=node.task.action,
                                target=node.task.target,
                                success=True,
                                result=str(
                                    node.task.result
                                ),
                                error="",
                                started=started,
                                completed=completed,
                            )
                        )

                    return True

                # =================================================
                # TOOL-LEVEL FAILURE
                # =================================================

                node.task.success = False
                node.task.completed = False
                node.task.error = str(
                    node.task.result
                )

                print(
                    "TASK FAILED:",
                    node.task.action,
                    node.task.target,
                )

                print(
                    "RESULT:",
                    node.task.result,
                )

                # =================================================
                # RETRY
                # =================================================

                if self.retry_manager.should_retry(
                    node.task
                ):

                    print(
                        "Retrying task..."
                    )

                    self.retry_manager.retry(
                        node.task
                    )

                    print(
                        "Retry attempt:",
                        node.task.retry_count,
                        "/",
                        node.task.max_retries,
                    )

                    continue

                # =================================================
                # PERMANENT FAILURE
                # =================================================

                node.failed = True
                node.completed = False
                node.running = False

                if (
                    self.execution_memory
                    is not None
                ):

                    self.execution_memory.add(
                        ExecutionRecord(
                            goal_id=goal_id or "",
                            action=node.task.action,
                            target=node.task.target,
                            success=False,
                            result=str(
                                node.task.result
                            ),
                            error=str(
                                node.task.error
                            ),
                            started=started,
                            completed=completed,
                        )
                    )

                return False

            except Exception as error:

                completed = datetime.now()

                node.task.success = False
                node.task.completed = False
                node.task.error = str(
                    error
                )

                print(
                    "TASK EXCEPTION:",
                    node.task.action,
                    node.task.target,
                )

                print(
                    "ERROR:",
                    error,
                )

                # =================================================
                # RETRY EXCEPTION
                # =================================================

                if self.retry_manager.should_retry(
                    node.task
                ):

                    print(
                        "Retrying after exception..."
                    )

                    self.retry_manager.retry(
                        node.task
                    )

                    print(
                        "Retry attempt:",
                        node.task.retry_count,
                        "/",
                        node.task.max_retries,
                    )

                    continue

                node.failed = True
                node.completed = False
                node.running = False

                if (
                    self.execution_memory
                    is not None
                ):

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

            if node.failed:

                responses.append(
                    f"Failed: {task.error}"
                )

                continue

            if task.result is not None:

                responses.append(
                    str(task.result)
                )

        if not responses:

            return "No results were produced."

        return "\n".join(
            responses
        )

    # ============================================================
    # CONTEXT TARGET RESOLUTION
    # ============================================================

    def _resolve_target(self, target):
        """
        Resolve context references in a task target.

        Supported references:

            $LAST_RESULT
            $LAST_UI
            $LAST_UI||text
            $LAST_ACTION
            $LAST_TARGET
            $RESULT:<action>
        """

        if target is None:
            return None

        if not isinstance(
            target,
            str,
        ):
            return target

        value = target.strip()

        if not value.startswith("$"):
            return target

        # ========================================================
        # LAST RESULT
        # ========================================================

        if value == "$LAST_RESULT":

            return self.task_context.get(
                "last_result"
            )

        # ========================================================
        # LAST UI + TEXT
        # ========================================================

        if value.startswith(
            "$LAST_UI||"
        ):

            text = value[
                len("$LAST_UI||"):
            ].strip()

            descriptor = (
                self.task_context.get(
                    "last_ui"
                )
            )

            if descriptor is None:
                return None

            return {
                "descriptor": descriptor,
                "text": text,
            }

        # ========================================================
        # LAST UI DESCRIPTOR
        # ========================================================

        if value == "$LAST_UI":

            return self.task_context.get(
                "last_ui"
            )

        # ========================================================
        # LAST ACTION
        # ========================================================

        if value == "$LAST_ACTION":

            return self.task_context.get(
                "last_action"
            )

        # ========================================================
        # LAST TARGET
        # ========================================================

        if value == "$LAST_TARGET":

            return self.task_context.get(
                "last_target"
            )

        # ========================================================
        # ACTION-SPECIFIC RESULT
        # ========================================================

        if value.startswith(
            "$RESULT:"
        ):

            action = value[
                len("$RESULT:"):
            ].strip()

            if not action:
                return None

            return self.task_context.get(
                f"result:{action}"
            )

        # Unknown reference:
        # leave it untouched so the tool can handle it.
        return target