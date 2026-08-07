from ai.workflow.task_queue import TaskQueue


class ExecutionManager:

    def __init__(self, brain):

        self.brain = brain

    def execute(self, context):

        queue = TaskQueue(context.tasks)

        if queue.empty():

            context.response = None
            return

        response = self.brain.execution_engine.execute(
            queue
        )

        context.response = response

        tasks = queue.to_list()

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

            print(type(response))
            print(response)
            self.brain.chat_memory.add(
                "Assistant",
                response,
            )

            self.brain.conversation_manager.remember_response(
                response,
            )