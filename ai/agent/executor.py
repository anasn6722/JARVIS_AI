class AgentExecutor:

    def __init__(self, brain):
        self.brain = brain

    
    
    def execute(self, tasks):
    
        responses = []
    
        total = len(tasks)
    
        print("=" * 60)
        print("WORKFLOW START")
        print("=" * 60)
    
        for index, task in enumerate(tasks, start=1):
        
            print(f"\nTASK {index}/{total}")
            print(f"Action : {task.action}")
            print(f"Target : {task.target}")
    
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
    
            response = self.brain.tool_executor.execute(
                task.action,
                task.target,
            )
    
            success = self.brain.agent_verifier.verify(
                task,
                response,
            )
    
            # -------------------------
            # Save execution state
            # -------------------------
    
            task.result = response or ""
            task.success = success
            task.completed = True
    
            if not success:
                task.error = response or "Unknown error"
    
            # -------------------------
            # Conversation memory
            # -------------------------
    
            if success:
            
                if task.action == "open":
                    self.brain.conversation_memory.remember_app(
                        task.target
                    )
    
                elif task.action == "close":
                    self.brain.conversation_memory.forget_app(
                        task.target
                    )
    
                elif task.action == "search":
                    self.brain.conversation_memory.remember_search(
                        task.target
                    )
    
            # -------------------------
            # Logging
            # -------------------------
    
            print("Success :", task.success)
    
            if task.success:
                print("Result  :", task.result)
            else:
                print("Error   :", task.error)
    
            if response:
                responses.append(response)
    
        print("=" * 60)
        print("WORKFLOW COMPLETE")
        print("=" * 60)
    
        return "\n".join(responses)
    
    
