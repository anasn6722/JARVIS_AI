from dataclasses import dataclass


@dataclass
class KnowledgeResult:

    success: bool

    source: str

    query: str

    content: str

    confidence: float = 1.0

    error: str = ""
