class AgentExecutor:

    def __init__(self, brain):
        self.brain = brain

        
    def execute(self, tasks):

        print("EXECUTOR RECEIVED:", tasks)
        responses = []

        for task in tasks:

            # -------------------------
            # Normalize AI Planner output
            # -------------------------

            if (
                task.action == "search"
                and "youtube" in task.target.lower()
            ):
                task.action = "youtube_search"
                task.target = (
                    task.target
                    .replace("youtube", "")
                    .strip()
                )

            if (
                task.action == "open"
                and task.target.lower() in self.brain.websites
            ):
                task.target = task.target.lower()


            print(
                f"Executing tool: {task.action} ({task.target})"
            )

            response = self.brain.tool_executor.execute(
                task.action,
                task.target,
            )

            print("TOOL RESPONSE:", response)

            if task.action == "open":
                self.brain.conversation_memory.remember_app(task.target)
            
            
            elif task.action == "close":
                self.brain.conversation_memory.forget_app(task.target)
            
            
            elif task.action == "search":
                self.brain.conversation_memory.remember_search(task.target)
                
            success = self.brain.agent_verifier.verify(
                task,
                response,
            )
            
            task.completed = success


            if response:
                responses.append(response)

            task.completed = True

        return "\n".join(responses)