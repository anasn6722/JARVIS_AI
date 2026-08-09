from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.resolver.window_resolver import WindowResolver


class DesktopController:
    """High-level controller for desktop window automation."""

    def __init__(self):
        self.window_manager = WindowManager()
        self.window_resolver = WindowResolver(self.window_manager)

    def list_windows(self):
        """Return all visible desktop windows."""
        return self.window_manager.list_windows()

    def get_active_window(self):
        """Return the currently active window."""
        return self.window_manager.get_active_window()


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

    