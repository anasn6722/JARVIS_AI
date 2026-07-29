from dataclasses import dataclass


@dataclass
class Task:
    action: str
    target: str = ""
    completed: bool = False