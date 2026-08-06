class ExecutionHandler:

    def __init__(self, brain):
        self.brain = brain

    # -----------------------------------
    # Available AI Tools
    # -----------------------------------

    def available_tools(self):

        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self.brain.tool_registry.all()
        ]

    # -----------------------------------
    # Planner Context
    # -----------------------------------

    def planner_context(self):

        last_tasks = getattr(
            self.brain.context,
            "last_tasks",
            [],
        )

        return f"""
Last App: {self.brain.context.last_app}

Last Search: {self.brain.context.last_search}

Current Goal: {self.brain.context.current_goal}

Previous Tasks:

{last_tasks}
"""

    # -----------------------------------
    # Builtin Commands
    # -----------------------------------

    def builtin(
        self,
        intent,
        command,
    ):

        response = self.brain.registry.execute(
            intent,
            command,
        )

        if response:

            self.brain.chat_memory.add(
                "Assistant",
                response,
            )

            self.brain.conversation_manager.remember_response(
                response
            )

        return response

    # -----------------------------------
    # Planner
    # -----------------------------------

    def planner(self, command_data):
        

        tasks = self.brain.planning_manager.plan(
            command_data
        )

        if not tasks:
            return None

        response = self.brain.execution_engine.execute(
            tasks
        )

        for task in tasks:

            if task.action == "open":

                self.brain.conversation_memory.remember_app(
                    task.target
                )

            elif task.action == "open_website":

                self.brain.conversation_memory.remember_website(
                    task.target
                )

        self.brain.context.last_tasks = tasks

        if response:

            self.brain.chat_memory.add(
                "Assistant",
                response,
            )

            self.brain.conversation_manager.remember_response(
                response
            )

        return response

    # -----------------------------------
    # Plugins
    # -----------------------------------

    def plugin(
        self,
        intent,
        command,
    ):

        response = self.brain.plugin_manager.execute(
            intent,
            command,
        )

        if response:

            self.brain.chat_memory.add(
                "Assistant",
                response,
            )

        return response