from ai.memory.execution.execution_memory import ExecutionMemory
from ai.workflow.event_bus import EventBus
from ai.workflow.graph_runner import GraphRunner
from ai.workflow.linear_runner import LinearRunner
from ai.workflow.retry_manager import RetryManager
from ai.workflow.scheduler import Scheduler
from core.hud_state import hud_state


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

        # =========================================================
        # EVENT BUS
        # =========================================================

        self.events = EventBus()

        self.events.subscribe(
            "WORKFLOW_STARTED",
            self._hud_workflow_started,
        )

        self.events.subscribe(
            "TASK_STARTED",
            self._hud_task_started,
        )

        self.events.subscribe(
            "TASK_COMPLETED",
            self._hud_task_completed,
        )

        self.events.subscribe(
            "TASK_FAILED",
            self._hud_task_failed,
        )

        self.events.subscribe(
            "WORKFLOW_FINISHED",
            self._hud_workflow_finished,
        )

        # =========================================================
        # SERVICES
        # =========================================================

        self.retry_manager = RetryManager()

        self.scheduler = Scheduler(
            self
        )

        self.linear_runner = LinearRunner(
            tool_executor,
        )

        self.graph_runner = GraphRunner(
            tool_executor,
            self.events,
            self.retry_manager,
            self.execution_memory,
        )

    # =========================================================
    # RUN
    # =========================================================

    def run(
        self,
        tasks=None,
        graph=None,
        goal_id=None,
    ):
        if graph is not None:

            print(
                ">>> USING GRAPH RUNNER"
            )

            return self.graph_runner.run(
                graph,
                goal_id=goal_id,
            )

        print(
            ">>> USING LINEAR RUNNER"
        )

        return self.linear_runner.run(
            tasks
        )

    # =========================================================
    # RUN ACTION
    # =========================================================

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

    # =========================================================
    # HUD EVENTS
    # =========================================================

    @staticmethod
    def _hud_workflow_started(event):
        hud_state.update(
            state="EXECUTING",
            event="WORKFLOW_STARTED",
            action="",
            target="",
            result="",
            progress=0,
            completed=0,
            total=(
                len(event.data.tasks)
                if event.data is not None
                and hasattr(event.data, "tasks")
                else 0
            ),
        )

    @staticmethod
    def _hud_task_started(event):
        task = event.task

        total = 0
        completed = 0

        if event.data is not None:
            completed = len(
                getattr(
                    event.data,
                    "completed",
                    [],
                )
            )

            total = len(
                getattr(
                    event.data,
                    "tasks",
                    [],
                )
            )

        progress = 0

        if total:
            progress = int(
                (
                    completed
                    / total
                )
                * 100
            )

        hud_state.update(
            state="EXECUTING",
            event="TASK_STARTED",
            action=getattr(
                task,
                "action",
                "",
            ),
            target=getattr(
                task,
                "target",
                "",
            ),
            result="",
            progress=progress,
            completed=completed,
            total=total,
        )

    @staticmethod
    def _hud_task_completed(event):
        task = event.task

        total = 0
        completed = 0

        if event.data is not None:
            completed = len(
                getattr(
                    event.data,
                    "completed",
                    [],
                )
            )

            total = len(
                getattr(
                    event.data,
                    "tasks",
                    [],
                )
            )

        progress = 0

        if total:
            progress = int(
                (
                    completed
                    / total
                )
                * 100
            )

        hud_state.update(
            state="EXECUTING",
            event="TASK_COMPLETED",
            action=getattr(
                task,
                "action",
                "",
            ),
            target=getattr(
                task,
                "target",
                "",
            ),
            result=getattr(
                task,
                "result",
                "",
            ),
            progress=progress,
            completed=completed,
            total=total,
        )

    @staticmethod
    def _hud_task_failed(event):
        task = event.task

        hud_state.update(
            state="ERROR",
            event="TASK_FAILED",
            action=getattr(
                task,
                "action",
                "",
            ),
            target=getattr(
                task,
                "target",
                "",
            ),
            result=getattr(
                task,
                "error",
                "",
            ),
        )

    @staticmethod
    def _hud_workflow_finished(event):
        data = event.data

        completed = 0
        total = 0
        failed = 0

        if data is not None:
            completed = len(
                getattr(
                    data,
                    "completed",
                    [],
                )
            )

            total = len(
                getattr(
                    data,
                    "tasks",
                    [],
                )
            )

            failed = len(
                getattr(
                    data,
                    "failed",
                    [],
                )
            )

        if failed:
            state = "ERROR"
        else:
            state = "IDLE"

        progress = 0

        if total:
            progress = int(
                (
                    completed
                    / total
                )
                * 100
            )

        hud_state.update(
            state=state,
            event="WORKFLOW_FINISHED",
            progress=progress,
            completed=completed,
            total=total,
        )