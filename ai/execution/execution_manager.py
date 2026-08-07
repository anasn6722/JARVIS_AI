from datetime import datetime

from ai.history.action_record import ActionRecord


class ExecutionManager:

    def __init__(
        self,
        execution_engine,
        conversation_memory,
        chat_memory,
        conversation_manager,
        context,
        action_history,
    ):
        self.execution_engine = execution_engine
        self.conversation_memory = conversation_memory
        self.chat_memory = chat_memory
        self.conversation_manager = conversation_manager
        self.context = context
        self.action_history = action_history

    def execute(self, context):

        tasks = context.tasks

        if not tasks:
            context.response = None
            return None

        response = self.execution_engine.execute(
            tasks=tasks,
            graph=context.graph,
        )

        context.response = response

        for task in tasks:

            # -------------------------
            # Save successful actions
            # -------------------------

            if task.success:

                undo_action = None
                undo_target = None
                
                if task.action == "open":
                
                    undo_action = "close"
                    undo_target = task.target
                
                elif task.action == "close":
                
                    undo_action = "open"
                    undo_target = task.target
                
                record = ActionRecord(
                    action=task.action,
                    target=task.target,
                    success=True,
                    response=task.result,
                    timestamp=datetime.now(),
                    undo_action=undo_action,
                    undo_target=undo_target,
                )

                self.action_history.add(record)

                # Temporary Debug
                print("=" * 50)
                print("ACTION HISTORY")

                for item in self.action_history.all():
                    print(item)

                print("=" * 50)

            # -------------------------
            # Conversation Memory
            # -------------------------

            if task.action == "open":

                self.conversation_memory.remember_app(
                    task.target
                )

            elif task.action == "open_website":

                self.conversation_memory.remember_website(
                    task.target
                )

        self.context.last_tasks = tasks

        if response:

            self.chat_memory.add(
                "Assistant",
                response,
            )

            self.conversation_manager.remember_response(
                response,
            )

        return response