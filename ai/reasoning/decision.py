from dataclasses import dataclass
from typing import Optional


@dataclass
class Decision:
    route: str          # MEMORY, TOOL, PLANNER, AI
    intent: str
    confidence: float = 1.0

    tool: Optional[str] = None
    reason: Optional[str] = None