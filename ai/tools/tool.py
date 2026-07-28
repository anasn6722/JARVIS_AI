from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    description: str
    callback: callable