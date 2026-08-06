class UndoManager:

    def __init__(
        self,
        action_history,
        workflow_manager,
    ):
        self.history = action_history
        self.workflow = workflow_manager

    def undo(self):

        record = self.history.last()

        if record is None:
            return "Nothing to undo."

        if record.undo_action is None:
            return "This action can't be undone."

        return self.workflow.run_action(
            record.undo_action,
            record.undo_target,
        )