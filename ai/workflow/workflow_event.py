from dataclasses import dataclass
from typing import Any


@dataclass
class WorkflowEvent:

    name: str

    task: Any = None

    data: Any = None