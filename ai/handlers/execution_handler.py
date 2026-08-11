from ai.memory.execution.execution_context import ExecutionContext
from ai.memory.execution.execution_history import ExecutionHistory
from ai.memory.execution.execution_memory import ExecutionMemory
from ai.memory.execution.execution_query import ExecutionQuery


class ExecutionHandler:

    def __init__(self, brain):
        self.brain = brain

        self.execution_memory = ExecutionMemory()
        self.execution_history = ExecutionHistory(
            self.execution_memory
        )
        self.execution_query = ExecutionQuery(
            self.execution_history
        )
        self.execution_context = ExecutionContext(
            self.execution_query
        )

    # -----------------------------------
    # Available AI Tools
    # -----------------------------------
    
    def available_tools(self):
    
        tools = self.brain.tool_registry.all()
    
        print("AVAILABLE TOOLS:")
        for tool in tools:
            print(
                "TYPE:",
                type(tool),
                "VALUE:",
                tool,
            )
    
        return [ 
            {   "name": tool.name, 
                "description": tool.description, 
            } 
                for tool in self.brain.tool_registry.all() 
        ]


    # -----------------------------------
    # Planner Context
    # -----------------------------------

    def planner_context(self):
        """Return current context information for planning."""

        last_tasks = getattr(
            self.brain.context,
            "last_tasks",
            [],
        )

        last_app = getattr(
            self.brain.context,
            "last_app",
            "",
        )

        last_search = getattr(
            self.brain.context,
            "last_search",
            "",
        )

        current_goal = getattr(
            self.brain.context,
            "current_goal",
            "",
        )

        execution_context = self.execution_context.recent(5)

        return f"""
    Last App: {last_app}
    
    Last Search: {last_search}
    
    Current Goal: {current_goal}
    
    Previous Tasks:
    {last_tasks}
    
    Recent Execution History:
    {execution_context}
    """
    # -----------------------------------
    # Builtin Commands
    # -----------------------------------

    def builtin(
        self,
        intent,
        command,
    ):
        """Execute a built-in command."""

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
        """Plan and execute a command."""

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
        """Execute a plugin command."""

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
