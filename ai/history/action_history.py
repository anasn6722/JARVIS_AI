class ActionHistory:

    def __init__(self):

        self._history = []
        self._redo = []

    def add(self, record):

        self._history.append(record)

        # New action clears redo stack
        self._redo.clear()

    def last(self):

        if not self._history:
            return None

        return self._history[-1]

    def pop(self):

        if not self._history:
            return None

        record = self._history.pop()

        self._redo.append(record)

        return record

    def redo(self):

        if not self._redo:
            return None

        record = self._redo.pop()

        self._history.append(record)

        return record

    def all(self):

        return self._history