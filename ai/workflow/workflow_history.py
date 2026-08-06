from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkflowRecord:

    workflow_id: int

    status: str

    started_at: datetime

    finished_at: datetime | None = None

    completed_tasks: int = 0

    failed_tasks: int = 0

    response: str = ""


class WorkflowHistory:

    def __init__(self):

        self.records = []

    def add(self, record):

        self.records.append(record)

    def latest(self):

        if not self.records:
            return None

        return self.records[-1]

    def all(self):

        return self.records