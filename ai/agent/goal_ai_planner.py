import json


class GoalAIPlanner:

    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, goal):

        prompt = f"""
You are an AI planning engine.

Break this goal into small actionable tasks.

Goal:

{goal}

Return ONLY JSON.

Example:

[
    "Install Python",
    "Install Django",
    "Create Project",
    "Views",
    "Templates"
]
"""

        response = self.llm.ask(prompt)

        try:
            return json.loads(response)

        except Exception:

            return []