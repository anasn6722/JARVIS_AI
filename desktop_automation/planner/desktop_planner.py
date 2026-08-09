from ai.agent.task import Task
from ai.planner.planner import Planner


class DesktopPlanner(Planner):
    """Plans desktop window automation commands."""

    DESKTOP_INTENTS = (
        "focus_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "active_window",
        "list_windows",
    )

    # Different names that can refer to the same application.
    WINDOW_ALIASES = {
        "vs code": "vscode",
        "visual studio code": "vscode",
        "visual studio": "vscode",
        "code": "vscode",
        "vscode": "vscode",
    }

    def can_plan(self, command):
        """Return True if this planner handles the command."""
        return command.intent in self.DESKTOP_INTENTS

    def normalize_window(self, window):
        """Normalize a window name to a canonical target."""
        window = str(window).strip().lower()

        return self.WINDOW_ALIASES.get(
            window,
            window,
        )

    def plan(self, command):
        """Create desktop automation tasks."""

        tasks = []

        intent = command.intent

        # =====================================================
        # WINDOW ACTIONS WITH TARGET
        # =====================================================

        target_window_intents = (
            "focus_window",
            "minimize_window",
            "maximize_window",
            "restore_window",
        )

        if intent in target_window_intents:

            windows = command.entities.get(
                "windows",
                [],
            )

            if not windows:
                return []

            # Normalize and remove duplicate aliases.
            normalized_windows = []

            for window in windows:
                normalized = self.normalize_window(window)

                if normalized not in normalized_windows:
                    normalized_windows.append(normalized)

            for window in normalized_windows:
                tasks.append(
                    Task(
                        action=intent,
                        target=window,
                    )
                )

        # =====================================================
        # ACTIVE WINDOW ACTIONS
        # =====================================================

        elif intent in (
            "minimize_active_window",
            "maximize_active_window",
            "restore_active_window",
        ):

            tasks.append(
                Task(
                    action=intent,
                    target="",
                )
            )

        # =====================================================
        # ACTIVE WINDOW
        # =====================================================

        elif intent == "active_window":

            tasks.append(
                Task(
                    action="active_window",
                    target="",
                )
            )

        # =====================================================
        # LIST WINDOWS
        # =====================================================

        elif intent == "list_windows":

            tasks.append(
                Task(
                    action="list_windows",
                    target="",
                )
            )

        # =====================================================
        # DEBUG
        # =====================================================

        print("=" * 50)
        print("DESKTOP PLANNER")

        for task in tasks:
            print(task)

        print("=" * 50)

        return tasks
