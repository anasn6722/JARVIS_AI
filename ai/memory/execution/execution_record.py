from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class ExecutionRecord:
    """Record one JARVIS tool execution."""
    
    
    goal_id: str
    action: str
    target: str = ""
    
    success: bool = False
    result: str = ""
    error: str = ""
    
    started: datetime | None = None
    completed: datetime | None = None
    
    id: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
    
        if self.started is None:
            self.started = datetime.now()
    
        if self.completed is None and self.success:
            self.completed = self.started
    