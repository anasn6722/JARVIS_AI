class DesktopPlanner:
    """Convert desktop commands into structured actions."""

    ACTIONS = {
        "show windows": "list_windows",
        "list windows": "list_windows",
        "active window": "active_window",
        "current window": "active_window",
        "focus": "focus_window",
        "focus window": "focus_window",
        "switch to": "focus_window",
        "minimize": "minimize_window",
        "minimize window": "minimize_window",
        "maximize": "maximize_window",
        "maximize window": "maximize_window",
        "restore": "restore_window",
        "restore window": "restore_window",
        "close": "close_window",
        "close window": "close_window",
    }

    def plan(self, command):
        """Convert a text command into an action and target."""

        if not command:
            return None

        command = command.lower().strip()

        # Commands without a target.
        if command in self.ACTIONS:
            action = self.ACTIONS[command]

            if action in {
                "list_windows",
                "active_window",
            }:
                return {
                    "action": action,
                    "target": None,
                }

        # Commands that require a target.
        for phrase, action in self.ACTIONS.items():
            if not command.startswith(phrase + " "):
                continue

            target = command[len(phrase):].strip()

            if not target:
                return None

            return {
                "action": action,
                "target": target,
            }

        return None