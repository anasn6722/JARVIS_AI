from collections import deque

from ai.agent.task import Task


class TaskQueue:

    def __init__(self, tasks=None):

        self._queue = deque(tasks or [])

    def add(self, task: Task):

        self._queue.append(task)

    def add_first(self, task: Task):

        self._queue.appendleft(task)

    def next(self):

        if self.empty():
            return None

        return self._queue.popleft()

    def peek(self):

        if self.empty():
            return None

        return self._queue[0]

    def empty(self):

        return len(self._queue) == 0

    def clear(self):

        self._queue.clear()

    def size(self):

        return len(self._queue)

    def __iter__(self):
        return iter(self._queue)

    def pending(self):
        return [
            task
            for task in self._queue
            if not task.completed
        ]

    def completed(self):
        return [
            task
            for task in self._queue
            if task.completed
        ]

    

    def remove(self, task):

        try:

            self._queue.remove(task)

            return True

        except ValueError:

            return False

    def to_list(self):

        return list(self._queue)