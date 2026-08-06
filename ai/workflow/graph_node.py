from dataclasses import dataclass, field


@dataclass
class GraphNode:

    id: str

    task: object

    children: list = field(default_factory=list)

    parents: list = field(default_factory=list)

    completed: bool = False