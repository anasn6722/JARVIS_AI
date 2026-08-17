from dataclasses import dataclass, field


@dataclass
class AgentResult:
    """Standard result returned by an agent."""

    success: bool
    response: str = ""
    data: object = None

    agent: str = ""
    error: str = ""

    metadata: dict = field(
        default_factory=dict
    )