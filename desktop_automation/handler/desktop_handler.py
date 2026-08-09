from desktop_automation.controller.desktop_controller import DesktopController
from desktop_automation.planner.desktop_planner import DesktopPlanner


class DesktopHandler:
    """Handle high-level desktop automation actions."""

    def __init__(self):
        self.desktop = DesktopController()
        self.planner = DesktopPlanner()

    def execute(self, command):
        """Plan and execute a natural-language desktop command."""

        plan = self.planner.plan(command)

        if not plan:
            return False, f"Could not understand desktop command: {command}"

        action = plan["action"]
        target = plan["target"]

        return self.handle(action, target)

    def handle(self, action, target=None):
        """Execute a structured desktop automation action."""

        if action == "list_windows":
            return True, self.desktop.list_windows()

        if action == "active_window":
            return True, self.desktop.get_active_window()

        if not target:
            return False, "A target window is required."

        if action == "find_window":
            window = self.desktop.find_window(target)

            if window:
                return True, window

            return False, f"Window not found: {target}"

        if action == "focus_window":
            return self.desktop.focus_window(target)

        if action == "minimize_window":
            return self.desktop.minimize_window(target)

        if action == "maximize_window":
            return self.desktop.maximize_window(target)

        if action == "restore_window":
            return self.desktop.restore_window(target)

        if action == "close_window":
            return self.desktop.close_window(target)

        return False, f"Unknown desktop action: {action}"