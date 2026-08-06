from dataclasses import dataclass, field

from ai.agent.task import Task


@dataclass
class Goal:

    id: str

    title: str

    description: str = ""

    tasks: list[Task] = field(default_factory=list)

    completed: bool = False 