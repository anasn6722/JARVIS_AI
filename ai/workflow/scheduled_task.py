from dataclasses import dataclass, field
from datetime import datetime

from ai.agent.task import Task


@dataclass(order=True)
class ScheduledTask:

    run_at: datetime

    task: Task = field(
        compare=False
    )

    executed: bool = field(
        default=False,
        compare=False
    )

    cancelled: bool = field(
        default=False,
        compare=False
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        compare=False
    )