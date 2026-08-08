
from automation.desktop.window_manager import WindowManager


class DesktopController:
    """High-level controller for Windows desktop automation."""

    def __init__(self):
        self.window_manager = WindowManager

    # =====================================================
    # WINDOWS
    # =====================================================

    def list_windows(self):
        """Return all visible windows."""

        return self.window_manager.list_windows()

    def active_window(self):
        """Return the currently active window."""

        return self.window_manager.get_active_window()

    def find_window(self, name):
        """Find a window by title."""

        return self.window_manager.find_window(
            name
        )

    def focus_window(self, name):
        """Find and focus a window."""

        window = self.find_window(name)

        if not window:
            return (
                False,
                f"I couldn't find a window called {name}.",
            )

        success = self.window_manager.focus_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't focus {window['title']}.",
            )

        return (
            True,
            f"Focused {window['title']}.",
        )

    def close_window(self, name):
        """Find and close a specific window."""

        window = self.find_window(name)

        if not window:
            return (
                False,
                f"I couldn't find a window called {name}.",
            )

        success = self.window_manager.close_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't close {window['title']}.",
            )

        return (
            True,
            f"Closed {window['title']}.",
        )

    def close_active_window(self):
        """Close the currently active window."""

        window = self.active_window()

        if not window:
            return (
                False,
                "I couldn't determine the active window.",
            )

        success = self.window_manager.close_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't close {window['title']}.",
            )

        return (
            True,
            f"Closed {window['title']}.",
        )