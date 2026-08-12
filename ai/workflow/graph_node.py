from dataclasses import dataclass, field

from ai.agent.task import Task


@dataclass
class GraphNode:
    id: str
    task: Task

    children: list[str] = field(default_factory=list)
    parents: list[str] = field(default_factory=list)

    completed: bool = False
    running: bool = False
    failed: bool = False
    blocked: bool = False

    @property
    def ready(self) -> bool:
        """Return True when this node is ready to execute."""

        if self.completed:
            return False

        if self.failed:
            return False

        if self.blocked:
            return False

        if self.running:
            return False

        return True