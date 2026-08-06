from dataclasses import dataclass, field


@dataclass
class WorkflowResult:

    success: bool = True

    response: str = ""

    errors: list[str] = field(default_factory=list)

    completed_tasks: int = 0

    failed_tasks: int = 0