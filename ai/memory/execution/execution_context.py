from ai.memory.execution.execution_query import ExecutionQuery


class ExecutionContext:
    """Build readable AI context from execution history."""

    def __init__(self, query: ExecutionQuery):
        self.query = query

    def recent(self, limit=5):
        """Build context from recent executions."""

        executions = self.query.recent(limit)

        if not executions:
            return "No recent executions."

        lines = [
            "Recent JARVIS activity:",
        ]

        for execution in executions:
            status = (
                "successful"
                if execution.success
                else "failed"
            )

            lines.append(
                f"- {execution.action} -> {status}"
            )

            if execution.result:
                lines.append(
                    f"  Result: {execution.result}"
                )

            if execution.error:
                lines.append(
                    f"  Error: {execution.error}"
                )

        return "\n".join(lines)

    def last(self):
        """Build context for the last execution."""

        execution = self.query.last()

        if not execution:
            return "No previous execution."

        status = (
            "successful"
            if execution.success
            else "failed"
        )

        lines = [
            f"Last action: {execution.action}",
            f"Status: {status}",
        ]

        if execution.result:
            lines.append(
                f"Result: {execution.result}"
            )

        if execution.error:
            lines.append(
                f"Error: {execution.error}"
            )

        return "\n".join(lines)

    def summary(self):
        """Build readable execution statistics."""

        summary = self.query.summary()

        return (
            "Execution summary:\n"
            f"Total: {summary['total']}\n"
            f"Successful: {summary['successful']}\n"
            f"Failed: {summary['failed']}"
        )