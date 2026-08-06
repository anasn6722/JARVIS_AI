class RedoManager:

    def __init__(
        self,
        action_history,
        workflow_manager,
    ):
        self.history = action_history
        self.workflow = workflow_manager

    def redo(self):

        record = self.history.redo()

        if record is None:
            return "Nothing to redo."

        return self.workflow.run_action(
            record.action,
            record.target,
        )