class WorkflowLogger:

    def __init__(self, bus):

        bus.subscribe(
            "WORKFLOW_STARTED",
            self.started,
        )

        bus.subscribe(
            "TASK_STARTED",
            self.task_started,
        )

        bus.subscribe(
            "TASK_COMPLETED",
            self.task_completed,
        )

        bus.subscribe(
            "TASK_FAILED",
            self.task_failed,
        )

        bus.subscribe(
            "WORKFLOW_FINISHED",
            self.finished,
        )

    def started(self, event):

        print("\nEVENT -> Workflow Started")

    def task_started(self, event):

        print(
            "EVENT -> Task Started:",
            event.task.action,
        )

    def task_completed(self, event):

        print(
            "EVENT -> Task Completed:",
            event.task.action,
        )

    def task_failed(self, event):

        print(
            "EVENT -> Task Failed:",
            event.task.action,
        )

    def finished(self, event):

        print("EVENT -> Workflow Finished\n")