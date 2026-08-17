from PySide6.QtCore import QObject, Signal


class BrainWorker(QObject):
    """Run Brain processing inside the worker thread."""

    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, command):
        super().__init__()

        self.command = command
        self.brain = None

    def run(self):
        try:
            # IMPORTANT:
            # Brain must be created inside this worker thread.
            # Its SQLite-backed memory objects are then created
            # in the same thread that uses them.
            from ai.brain import Brain

            self.brain = Brain()

            response = self.brain.process(
                self.command
            )

            self.finished.emit(
                response
            )

        except Exception as error:
            self.failed.emit(
                str(error)
            )