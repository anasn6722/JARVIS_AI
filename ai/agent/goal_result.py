from dataclasses import dataclass, field


@dataclass
class GoalResult:
    """Represent the result of executing a JARVIS goal."""

    success: bool = False
    message: str = ""
    results: list = field(default_factory=list)
    error: str = ""