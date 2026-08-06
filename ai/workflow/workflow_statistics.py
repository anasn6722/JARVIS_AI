class WorkflowStatistics:

    def __init__(self):

        self.total = 0

        self.completed = 0

        self.failed = 0

        self.cancelled = 0

    def workflow_completed(self):

        self.total += 1

        self.completed += 1

    def workflow_failed(self):

        self.total += 1

        self.failed += 1

    def workflow_cancelled(self):

        self.total += 1

        self.cancelled += 1

    @property
    def success_rate(self):

        if self.total == 0:
            return 0

        return (
            self.completed
            / self.total
        ) * 100