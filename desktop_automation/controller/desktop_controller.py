from desktop_automation.controller.mouse_controller import (
    MouseController,
)
from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.resolver.window_resolver import WindowResolver


class DesktopController:
    """High-level controller for desktop window automation."""

    def __init__(self):
        self.window_manager = WindowManager()
        self.window_resolver = WindowResolver(self.window_manager)
        self.mouse = MouseController()

    def list_windows(self):
        """Return all visible desktop windows."""
        return self.window_manager.list_windows()

    def get_active_window(self):
        """Return the currently active window."""
        return self.window_manager.get_active_window()

        
    def minimize_active_window(self):
        """Minimize the currently active window."""
        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.minimize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Minimized {window['title']}."

        return False, f"Could not minimize {window['title']}."


    def maximize_active_window(self):
        """Maximize the currently active window."""
        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.maximize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Maximized {window['title']}."

        return False, f"Could not maximize {window['title']}."


    def restore_active_window(self):
        """Restore the currently active window."""
        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.restore_window(
            window["hwnd"]
        )

        if success:
            return True, f"Restored {window['title']}."

        return False, f"Could not restore {window['title']}."



    def find_window(self, name):
        """Find a window by its natural name."""
        window = self.window_resolver.resolve(name)

        if not window:
            return None

        return window

    def close_window(self, name):
        """Find and close a window."""
        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.close_window(
            window["hwnd"]
        )

        if success:
            return True, f"Closed {window['title']}."

        return False, f"Could not close {window['title']}."

    
    def focus_window(self, name):
        """Find and focus a window by its natural name."""
        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.focus_window(window["hwnd"])

        if success:
            return True, f"Focused {window['title']}."

        return False, f"Could not focus {window['title']}."

    def minimize_window(self, name):
        """Find and minimize a window."""
        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.minimize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Minimized {window['title']}."

        return False, f"Could not minimize {window['title']}."

    def maximize_window(self, name):
        """Find and maximize a window."""
        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.maximize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Maximized {window['title']}."

        return False, f"Could not maximize {window['title']}."

    def restore_window(self, name):
        """Find and restore a window."""
        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.restore_window(
            window["hwnd"]
        )

        if success:
            return True, f"Restored {window['title']}."

        return False, f"Could not restore {window['title']}."

    # =========================================================
    # MOUSE
    # =========================================================

    def mouse_position(self):
        """Return current mouse position."""

        x, y = self.mouse.position()

        return (
            True,
            f"Mouse position: ({x}, {y}).",
        )

    def mouse_move(self, target):
        """Move mouse using 'x,y' coordinates."""

        try:
            x, y = self._parse_coordinates(target)

            return self.mouse.move(x, y)

        except (TypeError, ValueError) as error:
        
            return (
                False,
                str(error),
            )

    def mouse_click(self, target=None):
        """Left-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)
                return self.mouse.left_click(x, y)

            return self.mouse.left_click()

        except (TypeError, ValueError) as error:
        
            return (
                False,
                str(error),
            )

    def mouse_double_click(self, target=None):
        """Double-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)
                return self.mouse.double_click(x, y)

            return self.mouse.double_click()

        except (TypeError, ValueError) as error:
        
            return (
                False,
                str(error),
            )

    def mouse_right_click(self, target=None):
        """Right-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)
                return self.mouse.right_click(x, y)

            return self.mouse.right_click()

        except (TypeError, ValueError) as error:
        
            return (
                False,
                str(error),
            )

    def mouse_middle_click(self, target=None):
        """Middle-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)
                return self.mouse.middle_click(x, y)

            return self.mouse.middle_click()

        except (TypeError, ValueError) as error:
        
            return (
                False,
                str(error),
            )

    def mouse_scroll(self, target):
        """Scroll using a positive or negative integer."""

        try:
            amount = int(str(target).strip())

        except (TypeError, ValueError):
        
            return (
                False,
                "Scroll amount must be an integer.",
            )

        return self.mouse.scroll(amount)

    @staticmethod
    def _parse_coordinates(target):
        """Parse coordinates from 'x,y'."""

        if not isinstance(target, str):
            raise ValueError(
                "Coordinates must be provided as 'x,y'."
            )

        parts = [
            part.strip()
            for part in target.split(",")
        ]

        if len(parts) != 2:
            raise ValueError(
                "Coordinates must use the format 'x,y'."
            )

        try:
            x = int(parts[0])
            y = int(parts[1])

        except ValueError as error:
            raise ValueError(
                "Coordinates must be integers."
            ) from error

        return x, y

