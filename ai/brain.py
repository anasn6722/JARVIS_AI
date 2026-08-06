

from ai.builders.registry_builder import RegistryBuilder
from ai.builders.service_builder import ServiceBuilder
from ai.builders.tool_registry_builder import ToolRegistryBuilder
from ai.pipeline.context import PipelineContext
from ai.pipeline.pipeline import Pipeline


class Brain:
    def __init__(self):
        

        ServiceBuilder.build(self)

        self.registry = RegistryBuilder.build(self)
        self.pipeline = Pipeline(self)
        ToolRegistryBuilder.build(self)

        print(self.tool_registry.tools.keys())
        

        
    def process(self, command: str) -> str:

        commands = self.command_splitter.split(command)
    
        responses: list[str] = []
    
        for cmd in commands:
            context = PipelineContext(cmd)
            self.pipeline.run(context)
    
            if context.response:
                responses.append(context.response)
    
        return "\n".join(responses)     

    def handle_hello(self, command):
        return self.chat_handler.hello()

    def handle_identity(self, command):
        return self.chat_handler.identity()

    def handle_time(self, command):
        return self.chat_handler.time()

    def handle_search(self, command):
        return self.chat_handler.search(command)

    def handle_youtube(self, command):
        return self.chat_handler.youtube(command)
    

    def handle_last_message(self, command):
        return self.memory_handler.last_message()


    def handle_history(self, command):
        return self.memory_handler.history()


    def handle_set_name(self, command):
        return self.memory_handler.set_name(command)


    def handle_get_name(self, command):
        return self.memory_handler.get_name()


    def handle_set_preference(self, command):
        return self.memory_handler.set_preference(command)


    def handle_get_preference(self, command):
        return self.memory_handler.get_preference(command)
    
    def available_tools(self):
        return self.execution_handler.available_tools()

    
    
    def planner_context(self):
        return self.execution_handler.planner_context()

    
    def execute_builtin(
        self,
        intent,
        command,
    ):
        return self.execution_handler.builtin(
            intent,
            command,
        )

    def execute_planner(
        self,
        command_data,
    ):
        return self.execution_handler.planner(
            command_data
        )
    
    def execute_plugin(
        self,
        intent,
        command,
    ):
        return self.execution_handler.plugin(
            intent,
            command,
        )

    def handle_add_goal(self, command):
        return self.goal_handler.add_goal(command)

    def handle_show_goals(self, command):
        return self.goal_handler.show_goals()

    def handle_next_task(self, command):
        return self.goal_handler.next_task()

    def handle_complete_task(self, command):
        return self.goal_handler.complete_task()

    def handle_goal_progress(self, command):
        return self.goal_handler.progress()

    def handle_delete_goal(self, command):
        return self.goal_handler.delete_goal()

    


if __name__ == "__main__":
        brain = Brain()

        print(
            brain.process_agent(
                "open chrome then search python classes and tell me the time"
            )
        )