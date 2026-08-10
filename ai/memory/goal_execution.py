
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GoalExecution:
    """Represent one execution event for a JARVIS goal."""

    goal_id: str
    action: str
    target: str = ""

    started: datetime | None = None
    completed: datetime | None = None

    success: bool = False

    result: str = ""
    error: str = ""
