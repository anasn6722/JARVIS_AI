import json

from ai.agent.task import Task


class AIPlanner:
    """Creates executable tasks using the configured LLM."""

    def __init__(self, llm):
        self.llm = llm

    def plan(
        self,
        command,
        tools,
        context,
    ):
        """Generate a list of tasks for a command."""

        tool_list = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in tools
        )

        prompt = f"""
You are the planning engine for an AI assistant called JARVIS.

Your job is ONLY to create a task list.

Available tools:

{tool_list}

Current Context:

{context}

Rules:

1. Use ONLY the tools listed above.
2. Never invent tool names.
3. Never use "open" unless the target is an available application.
4. Music or videos → youtube_search.
5. Web questions → search.
6. Greetings → chat.
7. Return ONLY valid JSON.
8. Every task must contain:
   - action
   - target
9. Do NOT explain anything.

Example:

User:
Open Chrome then search Python classes

Output:

[
    {{
        "action": "open",
        "target": "chrome"
    }},
    {{
        "action": "search",
        "target": "python classes"
    }}
]

Example:

User:
Play Believer song

Output:

[
    {{
        "action": "youtube_search",
        "target": "Believer song"
    }}
]

Now plan this command:

{command}
"""

        response = self.llm.ask(
            prompt=prompt,
            history=None,
            name="JARVIS Planner",
        )

        if not response:
            return []

        # -------------------------
        # Clean LLM response
        # -------------------------

        response = response.strip()

        if response.startswith("```"):
            response = (
                response
                .replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        # -------------------------
        # Parse JSON
        # -------------------------

        try:
            data = json.loads(response)

        except json.JSONDecodeError as exc:
            print("=" * 60)
            print("AI PLANNER JSON ERROR")
            print(exc)
            print("RAW RESPONSE:")
            print(response)
            print("=" * 60)

            return []

        # -------------------------
        # Validate result
        # -------------------------

        if not isinstance(data, list):
            print(
                "AI Planner returned "
                "something other than a task list."
            )
            return []
        valid_actions = {
            tool["name"]
            for tool in tools
        }

        tasks = []

        for item in data:
            if not isinstance(item, dict):
                continue
            
            action = item.get("action")
            target = item.get("target", "")
        
            if not action:
                continue
            
            if action not in valid_actions:
                print(
                    f"AI Planner: Ignoring unknown tool: {action}"
                )
                continue
            
            tasks.append(
                Task(
                    action=action,
                    target=target,
                )
            )
        
        return tasks