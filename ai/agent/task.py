from dataclasses import dataclass


@dataclass
class Task:
    action: str
    target: str = ""

    completed: bool = False
    success: bool = False

    retry_count: int = 0
    max_retries: int = 2

    result: str = ""
    error: str = ""