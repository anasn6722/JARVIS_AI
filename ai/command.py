from dataclasses import dataclass, field
from typing import Any


@dataclass
class Command:
    # Original user request
    original: str

    # Classified intent
    intent: str
    destination: str

    # Extracted entities
    entities: dict[str, Any] = field(default_factory=dict)

    # Goal detection
    goal: str | None = None

    # Goal tracking
    goal_id: str |None = None
    parent_goal: str | None = None

    # Planning
    requires_planning: bool = False

    # Execution metadata
    confidence: float = 1.0