import json


class GoalAIPlanner:

    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, goal: str):

        prompt = f"""
You are an AI task planner.

Break the following goal into executable tasks.

Goal:
{goal}

Return ONLY valid JSON.

Example:

[
    {{
        "action": "install",
        "target": "python"
    }},
    {{
        "action": "install",
        "target": "django"
    }},
    {{
        "action": "create_project",
        "target": "portfolio"
    }}
]
"""

        response = self.llm.ask(prompt)

        try:
            return json.loads(response)

        except Exception as e:
            print("GoalAIPlanner Error:", e)
            return []