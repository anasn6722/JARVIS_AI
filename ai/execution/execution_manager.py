
from datetime import datetime

from ai.history.action_record import ActionRecord
from brain.services import WEBSITES


class ExecutionManager:
    """Manages task execution, history, and conversation memory."""

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

    # ============================================================
    # EXECUTE TASKS
    # ============================================================

    def execute(self, context):
        """Execute planned tasks and update memory."""

        tasks = context.tasks

        # --------------------------------------------------------
        # NO TASKS
        # --------------------------------------------------------

        if not tasks:
            context.response = None
            return None

        # --------------------------------------------------------
        # EXECUTION ENGINE
        # --------------------------------------------------------

        response = self.execution_engine.execute(
            tasks=tasks,
            graph=context.graph,
        )

        context.response = response

        # ========================================================
        # PROCESS TASK RESULTS
        # ========================================================

        for task in tasks:

            # ----------------------------------------------------
            # SUCCESSFUL ACTION
            # ----------------------------------------------------

            if task.success:

                self._save_action_history(task)

                self._update_conversation_memory(task)

        # ========================================================
        # SAVE LAST TASKS
        # ========================================================

        self.context.last_tasks = tasks

        # ========================================================
        # CHAT MEMORY
        # ========================================================

        if response:

            self.chat_memory.add(
                "Assistant",
                response,
            )

            self.conversation_manager.remember_response(
                response,
            )

        return response

    # ============================================================
    # ACTION HISTORY
    # ============================================================

    def _save_action_history(self, task):
        """Save a successful task to action history."""

        undo_action = None
        undo_target = None

        # --------------------------------------------------------
        # OPEN
        # --------------------------------------------------------

        if task.action == "open":

            undo_action = "close"
            undo_target = task.target

        # --------------------------------------------------------
        # CLOSE
        # --------------------------------------------------------

        elif task.action == "close":

            undo_action = "open"
            undo_target = task.target

        # --------------------------------------------------------
        # CREATE RECORD
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # DEBUG
        # --------------------------------------------------------

        print("=" * 50)
        print("ACTION HISTORY")

        for item in self.action_history.all():
            print(item)

        print("=" * 50)

    # ============================================================
    # CONVERSATION MEMORY
    # ============================================================

    def _update_conversation_memory(self, task):
        """Update short-term memory after a successful action."""

        target = task.target

        if not target:
            return

        # ========================================================
        # OPEN
        # ========================================================

        if task.action == "open":

            target_lower = target.lower().strip()

            # ----------------------------------------------------
            # WEBSITE
            # ----------------------------------------------------

            if target_lower in WEBSITES:

                self.conversation_memory.remember_website(
                    target
                )

                print(
                    f"🧠 Memory: website = {target}"
                )

            # ----------------------------------------------------
            # APPLICATION
            # ----------------------------------------------------

            else:

                self.conversation_memory.remember_app(
                    target
                )

                print(
                    f"🧠 Memory: app = {target}"
                )

        # ========================================================
        # CLOSE
        # ========================================================

        elif task.action == "close":

            target_lower = target.lower().strip()

            # ----------------------------------------------------
            # CLOSED WEBSITE
            # ----------------------------------------------------

            if target_lower in WEBSITES:

                self.conversation_memory.forget_website(
                    target
                )

                print(
                    f"🧠 Memory: removed website = {target}"
                )

            # ----------------------------------------------------
            # CLOSED APPLICATION
            # ----------------------------------------------------

            else:

                self.conversation_memory.forget_app(
                    target
                )

                print(
                    f"🧠 Memory: removed app = {target}"
                )