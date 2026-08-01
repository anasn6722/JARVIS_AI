import json

from ai.agent.task import Task


class AIPlanner:

    def __init__(self, llm):
        self.llm = llm

    def plan(
        self,
        command,
        tools,
        context,
    ):

        tool_list = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in tools
        )

        prompt = f"""
        You are the planning engine for an AI assistant called JARVIS.
        
        Your job is ONLY to create a task list.
        
        Available tools:
        
        {tool_list}
        
        Rules:
        
        1. Use ONLY the tools above.
        2. Never invent tool names.
        3. Never use "open" unless the target is an available application.
        4. Music or videos → youtube_search.
        5. Web questions → search.
        6. Greetings → chat.
        7. Return ONLY valid JSON.
        Every task must contain:

        action
        target
        
        Never leave target empty.
        8. Do NOT explain anything.
        
        Example 1
        Current Context

        {context}
        
        User:
        Open Chrome then search Python classes
        
        Output:
        
        [
            {{
                "action":"open",
                "target":"chrome"
            }},
            {{
                "action":"search",
                "target":"python classes"
            }}
        ]
        
        Example 2
        
        User:
        Play Believer song
        
        Output:
        
        [
            {{
                "action":"youtube_search",
                "target":"Believer song"
            }}
        ]
        
        Now plan this command:
        
        {command}
        """

        response = self.llm.ask(prompt)

        # parse JSON here...

        try:
            data = json.loads(response)

        except json.JSONDecodeError:
        
            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            data = json.loads(response)