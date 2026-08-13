from ai.agent.task import Task


class RecoveryManager:
    """Decides whether a failed task can be recovered."""

    def __init__(
        self,
        llm,
        available_tools_provider,
        execution_context_provider,
    ):
        self.llm = llm
        self.available_tools_provider = available_tools_provider
        self.execution_context_provider = execution_context_provider

    def recover(
        self,
        task,
    ) -> Task | None:
        """Generate an alternative task for a failed task."""

        context = self.execution_context_provider()

        tools = self.available_tools_provider()

        tool_list = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in tools
        )

        prompt = f"""
You are JARVIS recovery planner.

A task failed during execution.

Failed task:
Action: {task.action}
Target: {task.target}
Error: {task.error}
Previous result: {task.result}
Retry count: {task.retry_count}

Recent execution context:
{context}

Available tools:
{tool_list}

Your job is to decide whether the task can be recovered.

Rules:

1. Use only the available tools.
2. Do not repeat the exact failed task.
3. Return ONLY valid JSON.
4. If recovery is impossible, return null.
5. If recovery is possible, return:

{{
    "action": "tool_name",
    "target": "target"
}}

Do not explain anything.
"""

        response = self.llm.ask(
            prompt=prompt,
            history=None,
            name="JARVIS Recovery",
        )

        if not response:
            return None

        response = response.strip()

        if response.startswith("```"):
            response = (
                response
                .replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        import json

        try:
            data = json.loads(response)

        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None

        action = data.get("action")
        target = data.get("target", "")

        if not action:
            return None

        valid_tools = {
            tool["name"]
            for tool in tools
        }

        if action not in valid_tools:
            return None

        if (
            action == task.action
            and target.strip().lower()
            == task.target.strip().lower()
        ):
            return None

        return Task(
            action=action,
            target=target,
        )