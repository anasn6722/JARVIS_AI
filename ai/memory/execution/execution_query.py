from ai.memory.execution.execution_history import ExecutionHistory


class ExecutionQuery:
    """Query JARVIS execution history."""

    def __init__(self, history: ExecutionHistory):
        self.history = history

    def last(self):
        """Return the most recent execution."""
        return self.history.last()

    def recent(self, limit=10):
        """Return recent executions."""
        return self.history.recent(limit)

    def by_goal(self, goal_id):
        """Return executions for a specific goal."""
        return self.history.by_goal(goal_id)

    def by_action(self, action):
        """Return executions for a specific action."""
        return self.history.by_action(action)

    def successful(self):
        """Return successful executions."""
        return self.history.successful()

    def failed(self):
        """Return failed executions."""
        return self.history.failed()

    def today(self):
        """Return today's executions."""
        return self.history.today()

    def summary(self):
        """Return execution statistics."""
        return self.history.summary()