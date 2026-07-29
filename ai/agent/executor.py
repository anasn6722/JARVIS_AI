class AgentExecutor:
    def __init__(self, brain):
        self.brain = brain

    def execute(self, tasks):
        responses = []

        for task in tasks:
            print(task)

            if task.action == "open":
                responses.append(
                    self.brain.handle_open(task.target)
                )

            elif task.action == "search":
                responses.append(
                    self.brain.handle_search(task.target)
                )

            elif task.action == "get_time":
                responses.append(
                    self.brain.tool_executor.execute(
                    "get_time",
                    "",
                    )
                )

            elif task.action == "chat":
                responses.append(
                    self.brain.llm.ask(task.target)
                )

            task.completed = True

        return responses