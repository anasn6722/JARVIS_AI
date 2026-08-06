from dataclasses import dataclass, field

from ai.agent.task import Task
from ai.workflow.task_queue import TaskQueue
from ai.workflow.workflow_result import WorkflowResult
from ai.workflow.workflow_status import WorkflowStatus


@dataclass
class WorkflowContext:

    tasks: list[Task]

    queue: TaskQueue = field(init=False)

    current_index: int = 0

    current_task: Task | None = None

    completed: list[Task] = field(default_factory=list)

    failed: list[Task] = field(default_factory=list)

    variables: dict = field(default_factory=dict)

    results: dict = field(default_factory=dict)

    logs: list[str] = field(default_factory=list)

    status: WorkflowStatus = WorkflowStatus.PENDING

    cancelled: bool = False

    result: WorkflowResult = field(
        default_factory=WorkflowResult
    )

    @property
    def has_next(self):

        return not self.queue.empty()

    def next_task(self):

        task = self.queue.next()
    
        if task is None:
            return None
    
        self.current_task = task
    
        self.current_index += 1
    
        return task

    def __post_init__(self):

        self.queue = TaskQueue(self.tasks)