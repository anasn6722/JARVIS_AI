import json


class GoalAIPlanner:
    """Create executable task plans from high-level goals."""

    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry

    def create_plan(
       self,
       goal: str,
       context="",
    )   :
        tools = list(self.registry.all())

        if not tools:
            print("GoalAIPlanner: No tools registered.")
            return []

        tool_descriptions = "\n".join(
            f"- {tool.name}: {tool.description}"
            for tool in tools
        )

        prompt = f"""
You are an AI task planner for a desktop AI assistant.

Available tools:
{tool_descriptions}

Break the following goal into executable tasks.

Goal:
{goal}
Recent Context:
{context}

Rules:
1. Use ONLY the available tools.
2. The action must exactly match a tool name.
3. Do not invent tool names.
4. Use target only when required.
5. Return ONLY valid JSON.
6. Do not create presentation/report tasks unless such a tool exists.

Example:
[
    {{
        "action": "get_system_info",
        "target": null
    }},
    {{
        "action": "get_display_info",
        "target": null
    }},
    {{
        "action": "list_active_processes",
        "target": null
    }}
]
"""

        response = self.llm.ask(prompt)

        try:
            plan = json.loads(response)

            if not isinstance(plan, list):
                return []

            valid_tools = {
                tool.name
                for tool in tools
            }

            valid_plan = []

            for task in plan:
                action = task.get("action")

                if action not in valid_tools:
                    print(
                        f"GoalAIPlanner: Ignoring unknown tool: {action}"
                    )
                    continue

                valid_plan.append(task)

            return valid_plan

        except Exception as error:
            print(
                "GoalAIPlanner Error:",
                error,
            )
            return []