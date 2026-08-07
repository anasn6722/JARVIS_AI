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