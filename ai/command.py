from dataclasses import dataclass, field


@dataclass
class Command:
    original: str
    intent: str
    destination: str
    entities: dict = field(default_factory=dict)