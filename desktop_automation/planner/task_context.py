class TaskContext:
    """Store outputs produced by previously executed desktop tasks."""

    def __init__(self):
        self._values = {}

    def set(self, key, value):
        """Store a value."""
        self._values[str(key)] = value

    def get(self, key, default=None):
        """Return a stored value."""
        return self._values.get(
            str(key),
            default,
        )

    def has(self, key):
        """Return True when a key exists."""
        return str(key) in self._values

    def remove(self, key):
        """Remove a stored value."""
        self._values.pop(
            str(key),
            None,
        )

    def clear(self):
        """Clear all stored task context."""
        self._values.clear()

    def snapshot(self):
        """Return a copy of the current context."""
        return dict(self._values)

    def __repr__(self):
        return f"TaskContext({self._values!r})"