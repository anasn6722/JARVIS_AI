from ai.planner.planner import Planner


class DesktopPlanner(Planner):
    """Plan desktop window and mouse automation commands."""

    DESKTOP_INTENTS = {
        # Window control
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
        # Mouse control
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll_up",
        "mouse_scroll_down",
    }

    ACTIONS = {
        # Window control
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
        # Mouse control
        "mouse_position": "mouse_position",
        "mouse_move": "mouse_move",
        "mouse_click": "mouse_click",
        "mouse_double_click": "mouse_double_click",
        "mouse_right_click": "mouse_right_click",
        "mouse_middle_click": "mouse_middle_click",
        "mouse_scroll_up": "mouse_scroll",
        "mouse_scroll_down": "mouse_scroll",
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

        entities = getattr(
            command,
            "entities",
            {},
        ) or {}

        # =====================================================
        # MOUSE
        # =====================================================

        if action in {
            "mouse_move",
            "mouse_click",
            "mouse_double_click",
            "mouse_right_click",
            "mouse_middle_click",
        }:
            coordinates = entities.get(
                "coordinates",
                [],
            )

            if coordinates:
                target = coordinates[0]

            # A click without coordinates means:
            # click at the current cursor position.
            elif action in {
                "mouse_click",
                "mouse_double_click",
                "mouse_right_click",
                "mouse_middle_click",
            }:
                target = None

            else:
                return []

        elif action == "mouse_scroll":

            if command.intent == "mouse_scroll_up":
                target = "3"
            else:
                target = "-3"

        elif action == "mouse_position":

            target = None

        # =====================================================
        # WINDOWS
        # =====================================================

        else:

            windows = entities.get(
                "windows",
                [],
            )

            apps = entities.get(
                "apps",
                [],
            )

            if windows:
                target = windows[0]

            elif apps:
                target = apps[0]

            # Active-window actions don't require a target.
            if action in {
                "active_window",
                "list_windows",
                "close_active_window",
                "minimize_active_window",
                "maximize_active_window",
                "restore_active_window",
            }:
                target = None

        # =====================================================
        # CREATE TASK
        # =====================================================

        from ai.agent.task import Task

        task = Task(
            action=action,
            target=target,
        )

        return [task]