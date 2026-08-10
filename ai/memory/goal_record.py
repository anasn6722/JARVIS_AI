
from dataclasses import dataclass, field
from datetime import datetime

from ai.agent.goal_state import GoalState
from ai.agent.task import Task


@dataclass
class GoalRecord:
    id: str
    title: str
    created: datetime

    tasks: list[Task] = field(default_factory=list)

    completed: bool = False
    progress: float = 0.0

    paused: bool = False
    archived: bool = False

    state: GoalState = GoalState.PENDING

    description: str = ""
    metadata: dict = field(default_factory=dict)
