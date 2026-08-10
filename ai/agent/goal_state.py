from enum import Enum


class GoalState(str, Enum):
    """Possible states of a JARVIS goal."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"