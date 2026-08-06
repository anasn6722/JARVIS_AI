from dataclasses import dataclass
from datetime import datetime


@dataclass
class ActionRecord:

    action: str
    target: str

    success: bool

    response: str

    timestamp: datetime

    undo_action: str | None = None
    undo_target: str | None = None