import uuid
from dataclasses import dataclass, field


@dataclass
class Task:

    id: str = ""

    action: str = ""
    target: str = ""

    depends_on: list[str] = field(
        default_factory=list
    )

    completed: bool = False
    success: bool = False

    retry_count: int = 0
    max_retries: int = 2

    result: str = ""
    error: str = ""

    def __post_init__(self):

        if not self.id:
            self.id = str(uuid.uuid4())[:8]