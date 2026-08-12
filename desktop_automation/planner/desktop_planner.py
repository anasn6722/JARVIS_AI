from ai.planner.planner import Planner


class DesktopPlanner(Planner):
    """Plan desktop window automation commands."""

    DESKTOP_INTENTS = {
        "focus_window",
        "close_window",
        "close_active_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "active_window",
        "list_windows",
    }

    ACTIONS = {
        "focus_window": "focus_window",
        "close_window": "close_window",
        "close_active_window": "close_active_window",
        "minimize_window": "minimize_window",
        "maximize_window": "maximize_window",
        "restore_window": "restore_window",
        "minimize_active_window": "minimize_active_window",
        "maximize_active_window": "maximize_active_window",
        "restore_active_window": "restore_active_window",
        "active_window": "active_window",
        "list_windows": "list_windows",
    }

    def can_plan(self, command):
        """Return True when this planner handles the command."""

        if not command:
            return False

        return command.intent in self.DESKTOP_INTENTS

    def plan(self, command):
        """Convert a Command object into desktop Task objects."""

        if not self.can_plan(command):
            return []

        action = self.ACTIONS.get(command.intent)

        if not action:
            return []

        target = None

        if hasattr(command, "entities"):
            entities = command.entities or {}

            windows = entities.get("windows", [])
            apps = entities.get("apps", [])

            if windows:
                target = windows[0]

            elif apps:
                target = apps[0]

        # Some desktop actions operate on the active window.
        if action in {
            "active_window",
            "list_windows",
            "close_active_window",
            "minimize_active_window",
            "maximize_active_window",
            "restore_active_window",
        }:
            target = None

        # Import here to avoid unnecessary circular imports.
        from ai.agent.task import Task

        task = Task(
            action=action,
            target=target,
        )

        return [task]