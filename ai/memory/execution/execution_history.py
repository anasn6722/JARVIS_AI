from datetime import datetime

from ai.memory.execution.execution_memory import ExecutionMemory


class ExecutionHistory:
    """Provide history queries for JARVIS goal executions."""

    def __init__(
        self,
        execution_memory: ExecutionMemory,
    ):
        self.execution_memory = execution_memory

    # ========================================================
    # ALL
    # ========================================================

    def all(self):
        """Return all execution records."""
        return self.execution_memory.all()

    # ========================================================
    # BY GOAL
    # ========================================================

    def by_goal(self, goal_id):
        """Return executions belonging to one goal."""
        return [
            execution
            for execution in self.execution_memory.all()
            if execution.goal_id == goal_id
        ]

    # ========================================================
    # BY ACTION
    # ========================================================

    def by_action(self, action):
        """Return executions matching an action."""
        return [
            execution
            for execution in self.execution_memory.all()
            if execution.action == action
        ]

    # ========================================================
    # RECENT
    # ========================================================

    def recent(self, limit=10):
        """Return the most recent executions."""
        if limit <= 0:
            return []

        executions = self.execution_memory.all()

        return executions[-limit:]

    # ========================================================
    # LAST
    # ========================================================

    def last(self):
        """Return the most recent execution."""
        executions = self.execution_memory.all()

        if not executions:
            return None

        return executions[-1]

    # ========================================================
    # SUCCESSFUL
    # ========================================================

    def successful(self):
        """Return only successful executions."""
        return [
            execution
            for execution in self.execution_memory.all()
            if execution.success
        ]

    # ========================================================
    # FAILED
    # ========================================================

    def failed(self):
        """Return only failed executions."""
        return [
            execution
            for execution in self.execution_memory.all()
            if not execution.success
        ]

    # ========================================================
    # TODAY
    # ========================================================

    def today(self):
        """Return executions created today."""
        today = datetime.now().date()

        return [
            execution
            for execution in self.execution_memory.all()
            if (
                execution.started is not None
                and execution.started.date() == today
            )
        ]

    # ========================================================
    # COUNTS
    # ========================================================

    def successful_count(self):
        """Return the number of successful executions."""
        return len(self.successful())

    def failed_count(self):
        """Return the number of failed executions."""
        return len(self.failed())

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):
        """Return a summary of execution history."""
        executions = self.execution_memory.all()

        return {
            "total": len(executions),
            "successful": self.successful_count(),
            "failed": self.failed_count(),
        }

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):
        """Clear execution history."""
        self.execution_memory.clear()
