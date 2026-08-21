from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from threading import Lock

from ai.memory.execution.execution_record import ExecutionRecord
from ai.workflow.workflow_context import WorkflowContext
from ai.workflow.workflow_event import WorkflowEvent
from ai.workflow.workflow_status import WorkflowStatus
from desktop_automation.planner.task_context import TaskContext


class GraphRunner:
    """Execute tasks according to graph dependencies."""

    # ============================================================
    # ACTION SAFETY
    # ============================================================

    # These actions can affect desktop focus, visible UI state,
    # keyboard/mouse state, or shared UI references.
    SERIAL_ACTIONS = {
        "open",
        "close",
        "close_last",
        "focus_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "search_ui",
    }

    MAX_PARALLEL_WORKERS = 4

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

        # Shared task context for one graph.
        self.task_context = TaskContext()

        # Protect shared TaskContext writes when safe tasks execute
        # concurrently.
        self._context_lock = Lock()

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

        self.task_context.clear()

        context = WorkflowContext(
            [
                node.task
                for node in graph.nodes.values()
            ]
        )

        context.status = WorkflowStatus.RUNNING

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

            parallel_nodes = []
            serial_nodes = []

            for node in ready:

                if self._is_parallel_safe(
                    node
                ):
                    parallel_nodes.append(node)
                else:
                    serial_nodes.append(node)

            # ====================================================
            # PARALLEL SAFE NODES
            # ====================================================

            if parallel_nodes:

                print(
                    "=" * 60
                )

                print(
                    "PARALLEL EXECUTION"
                )

                print(
                    "Tasks:",
                    len(parallel_nodes),
                )

                for node in parallel_nodes:

                    print(
                        "Parallel:",
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

                worker_count = min(
                    self.MAX_PARALLEL_WORKERS,
                    len(parallel_nodes),
                )

                with ThreadPoolExecutor(
                    max_workers=worker_count,
                    thread_name_prefix="jarvis-task",
                ) as executor:

                    futures = {
                        executor.submit(
                            self.execute_node,
                            node,
                            goal_id,
                        ): node
                        for node in parallel_nodes
                    }

                    for future in as_completed(
                        futures
                    ):

                        node = futures[
                            future
                        ]

                        try:
                            future.result()

                        except Exception as error:

                            node.failed = True
                            node.running = False
                            node.task.success = False
                            node.task.completed = False
                            node.task.error = str(
                                error
                            )

                            print(
                                "Parallel task exception:",
                                error,
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

                print(
                    "=" * 60
                )

            # ====================================================
            # SERIAL DESKTOP / UI NODES
            # ====================================================

            for node in serial_nodes:

                if node.completed:
                    continue

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
        # CHECK COMPLETION
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
    # PARALLEL SAFETY
    # ============================================================

    @classmethod
    def _is_parallel_safe(cls, node):
        """
        Determine whether a task can safely run concurrently.

        Desktop/UI operations remain serialized because they may
        change focus, mouse position, keyboard state, browser
        state, or $LAST_UI.
        """

        action = str(
            node.task.action
            or ""
        ).strip().lower()

        if not action:
            return False

        if action in cls.SERIAL_ACTIONS:
            return False

        # Any UI-prefixed action is treated as unsafe by default.
        if action.startswith("ui_"):
            return False

        # Mouse/keyboard actions are always serialized.
        if (
            action.startswith("mouse_")
            or action.startswith("keyboard_")
        ):
            return False

        return True

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

                    success, message = (
                        raw_result
                    )

                    node.task.success = (
                        success
                    )

                    node.task.result = (
                        message
                    )

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
                    # SHARED TASK CONTEXT
                    # =============================================

                    with self._context_lock:

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
        """Build a human-readable response from task results."""

        responses = []

        for node in graph.nodes.values():

            task = node.task

            if node.failed:

                responses.append(
                    f"Failed: {task.error}"
                )

                continue

            if task.result is None:
                continue

            # =====================================================
            # UI FIND
            # =====================================================

            if task.action in {
                "ui_find_descriptor",
                "ui_describe",
            }:

                if isinstance(
                    task.result,
                    dict,
                ):

                    name = (
                        task.result.get(
                            "name"
                        )
                        or task.target
                        or "UI element"
                    )

                    responses.append(
                        f"Found {name}."
                    )

                    continue

            # =====================================================
            # UI CLICK
            # =====================================================

            if task.action == "ui_click_descriptor":

                target_name = None

                if isinstance(
                    task.result,
                    str,
                ):

                    target_name = (
                        task.result
                    )

                if (
                    isinstance(
                        task.target,
                        str,
                    )
                    and target_name is None
                ):

                    target_name = (
                        task.target
                    )

                if task.target == "$LAST_UI":

                    with self._context_lock:

                        descriptor = (
                            self.task_context.get(
                                "last_ui"
                            )
                        )

                    if isinstance(
                        descriptor,
                        dict,
                    ):

                        target_name = (
                            descriptor.get(
                                "name"
                            )
                            or "UI element"
                        )

                if target_name:

                    if str(
                        target_name
                    ).startswith(
                        "Clicked at"
                    ):

                        with self._context_lock:

                            descriptor = (
                                self.task_context.get(
                                    "last_ui"
                                )
                            )

                        if isinstance(
                            descriptor,
                            dict,
                        ):

                            target_name = (
                                descriptor.get(
                                    "name"
                                )
                                or "UI element"
                            )

                        else:

                            target_name = (
                                "UI element"
                            )

                    responses.append(
                        f"Clicked {target_name}."
                    )

                    continue

            # =====================================================
            # TYPING
            # =====================================================

            if task.action in {
                "ui_type_descriptor",
                "ui_type",
                "ui_type_at",
            }:

                result_text = str(
                    task.result
                )

                if result_text.startswith(
                    "Typed "
                ):

                    responses.append(
                        result_text
                    )

                else:

                    responses.append(
                        "Text entered successfully."
                    )

                continue

            # =====================================================
            # KEYBOARD
            # =====================================================

            if task.action == "keyboard_press":

                responses.append(
                    f"Pressed {task.target}."
                )

                continue

            if task.action == "keyboard_hotkey":

                responses.append(
                    f"Pressed {task.target}."
                )

                continue

            # =====================================================
            # OPEN / CLOSE
            # =====================================================

            if task.action == "open":

                responses.append(
                    f"Opened {task.target}."
                )

                continue

            if task.action == "close":

                responses.append(
                    f"Closed {task.target}."
                )

                continue

            # =====================================================
            # DEFAULT
            # =====================================================

            if isinstance(
                task.result,
                dict,
            ):

                name = task.result.get(
                    "name"
                )

                if name:

                    responses.append(
                        str(name)
                    )

                else:

                    responses.append(
                        "Task completed successfully."
                    )

            else:

                responses.append(
                    str(task.result)
                )

        if not responses:

            return (
                "Task completed successfully."
            )

        return "\n".join(
            responses
        )

    # ============================================================
    # CONTEXT TARGET RESOLUTION
    # ============================================================

    def _resolve_target(
        self,
        target,
    ):
        """
        Resolve context references.

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

            with self._context_lock:

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

            with self._context_lock:

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
        # LAST UI
        # ========================================================

        if value == "$LAST_UI":

            with self._context_lock:

                return self.task_context.get(
                    "last_ui"
                )

        # ========================================================
        # LAST ACTION
        # ========================================================

        if value == "$LAST_ACTION":

            with self._context_lock:

                return self.task_context.get(
                    "last_action"
                )

        # ========================================================
        # LAST TARGET
        # ========================================================

        if value == "$LAST_TARGET":

            with self._context_lock:

                return self.task_context.get(
                    "last_target"
                )

        # ========================================================
        # ACTION RESULT
        # ========================================================

        if value.startswith(
            "$RESULT:"
        ):

            action = value[
                len("$RESULT:"):
            ].strip()

            if not action:
                return None

            with self._context_lock:

                return self.task_context.get(
                    f"result:{action}"
                )

        return target