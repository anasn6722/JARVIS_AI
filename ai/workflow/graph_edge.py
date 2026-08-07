from dataclasses import dataclass


@dataclass
class GraphEdge:

    source: str

    target: str

    type: str = "depends_on"