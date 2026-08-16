from threading import Lock


class HudState:
    """Thread-safe runtime state shared with the JARVIS HUD."""

    MAX_HISTORY = 8

    def __init__(self):
        self._lock = Lock()

        self.state = "IDLE"
        self.event = "SYSTEM_READY"
        self.action = ""
        self.target = ""
        self.result = ""
        self.progress = 0
        self.completed = 0
        self.total = 0

        self.history = []

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        *,
        state=None,
        event=None,
        action=None,
        target=None,
        result=None,
        progress=None,
        completed=None,
        total=None,
    ):
        with self._lock:

            if state is not None:
                self.state = str(state)

            if event is not None:
                self.event = str(event)

            if action is not None:
                self.action = str(action)

            if target is not None:
                self.target = str(target)

            if result is not None:
                self.result = str(result)

            if progress is not None:
                self.progress = int(
                    max(
                        0,
                        min(
                            int(progress),
                            100,
                        ),
                    )
                )

            if completed is not None:
                self.completed = int(
                    max(
                        0,
                        completed,
                    )
                )

            if total is not None:
                self.total = int(
                    max(
                        0,
                        total,
                    )
                )

            # -------------------------------------------------
            # EVENT HISTORY
            # -------------------------------------------------

            if event is not None:

                item = {
                    "event": str(event),
                    "state": self.state,
                    "action": self.action,
                    "target": self.target,
                }

                self.history.insert(
                    0,
                    item,
                )

                self.history = self.history[
                    : self.MAX_HISTORY
                ]

    # =========================================================
    # SNAPSHOT
    # =========================================================

    def snapshot(self):
        with self._lock:

            return {
                "state": self.state,
                "event": self.event,
                "action": self.action,
                "target": self.target,
                "result": self.result,
                "progress": self.progress,
                "completed": self.completed,
                "total": self.total,
                "history": [
                    dict(item)
                    for item in self.history
                ],
            }


hud_state = HudState()