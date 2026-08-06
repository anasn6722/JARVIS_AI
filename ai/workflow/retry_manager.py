import time


class RetryManager:

    def __init__(self, delay=1):

        self.delay = delay

    def should_retry(self, task):

        return (
            task.retry_count
            < task.max_retries
        )

    def retry(self, task):

        task.retry_count += 1

        time.sleep(self.delay)

        return task