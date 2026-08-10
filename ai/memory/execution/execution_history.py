from ai.memory.execution.execution_memory import ExecutionMemory


class ExecutionHistory:
    """Provide history queries for JARVIS goal executions."""
    
    
    def __init__(self, execution_memory: ExecutionMemory):
        self.execution_memory = execution_memory
    
    def all(self):
        """Return all execution records."""
        return self.execution_memory.all()
    
    def by_goal(self, goal_id):
        """Return executions belonging to one goal."""
        return [
            execution
            for execution in self.execution_memory.all()
            if execution.goal_id == goal_id
        ]
    
    def recent(self, limit=10):
        """Return the most recent executions."""
        executions = self.execution_memory.all()
    
        return executions[-limit:]
    
    def last(self):
        """Return the most recent execution."""
        executions = self.execution_memory.all()
    
        if not executions:
            return None
    
        return executions[-1]
    
    def successful(self):
        """Return only successful executions."""
        return [
            execution
            for execution in self.execution_memory.all()
            if execution.success
        ]
    
    def failed(self):
        """Return only failed executions."""
        return [
            execution
            for execution in self.execution_memory.all()
            if not execution.success
        ]
    
    def clear(self):
        """Clear execution history."""
        self.execution_memory.clear()
    