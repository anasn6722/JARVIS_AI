from dataclasses import dataclass, field

from ai.agent.goal_state import GoalState
from ai.agent.task import Task


@dataclass
class Goal:
    """Represent a high-level JARVIS goal."""

    id: str
    title: str
    description: str = ""

    tasks: list[Task] = field(
        default_factory=list,
    )

    completed: bool = False
    progress: float = 0.0

    paused: bool = False
    archived: bool = False

    state: GoalState = GoalState.PENDING

    metadata: dict = field(
        default_factory=dict,
    )
