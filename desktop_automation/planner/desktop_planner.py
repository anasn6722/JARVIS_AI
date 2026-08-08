
from ai.agent.task import Task
from ai.planner.planner import Planner


class DesktopPlanner(Planner):
    """Plans desktop window automation commands."""

    DESKTOP_INTENTS = (
        "focus_window",
        "close_window",
        "close_active_window",
        "active_window",
        "list_windows",
    )

    def can_plan(self, command):
        return command.intent in self.DESKTOP_INTENTS

    def plan(self, command):
        tasks = []

        intent = command.intent

        # =====================================================
        # FOCUS WINDOW
        # =====================================================

        if intent == "focus_window":

            windows = command.entities.get(
                "windows",
                [],
            )

            if not windows:
                return []

            for window in windows:
                tasks.append(
                    Task(
                        action="focus_window",
                        target=window,
                    )
                )

        # =====================================================
        # CLOSE WINDOW
        # =====================================================

        elif intent == "close_window":

            windows = command.entities.get(
                "windows",
                [],
            )

            if not windows:
                return []

            for window in windows:
                tasks.append(
                    Task(
                        action="close_window",
                        target=window,
                    )
                )

        # =====================================================
        # CLOSE ACTIVE WINDOW
        # =====================================================

        elif intent == "close_active_window":

            tasks.append(
                Task(
                    action="close_active_window",
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
