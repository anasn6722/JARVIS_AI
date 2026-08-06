class WorkflowRetry:

    def __init__(self, brain):

        self.brain = brain

    def should_retry(self, task):

        return (
            task.retry_count
            <
            task.max_retries
        )

    def increase(self, task):

        task.retry_count += 1