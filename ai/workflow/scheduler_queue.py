import heapq


class SchedulerQueue:


    def __init__(self):

        self.queue = []


    def add(self, scheduled_task):

        heapq.heappush(
            self.queue,
            scheduled_task
        )


    def next(self):

        if not self.queue:

            return None

        return heapq.heappop(
            self.queue
        )


    def peek(self):

        if not self.queue:

            return None

        return self.queue[0]


    def empty(self):

        return len(self.queue) == 0