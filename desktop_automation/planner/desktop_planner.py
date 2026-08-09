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

    def can_plan(self, command):
        """Return True if this planner handles the command."""

        return command.intent in self.DESKTOP_INTENTS

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

            # Prefer explicit window entities.
            windows = command.entities.get(
                "windows",
                [],
            )

            # Fall back to application entities.
            if not windows:

                windows = command.entities.get(
                    "apps",
                    [],
                )

            if not windows:
                return []

            for window in windows:

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
