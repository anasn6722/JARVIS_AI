from itertools import count


class WorkflowID:

    _counter = count(1)

    @classmethod
    def next(cls):

        return next(cls._counter)