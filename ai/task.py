from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    action: str
    target: Any = None