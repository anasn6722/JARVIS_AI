
from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.resolver.window_resolver import WindowResolver


class DesktopController:
    """High-level controller for Windows desktop automation."""

    def __init__(self):
        self.window_manager = WindowManager()
        self.window_resolver = WindowResolver(
            self.window_manager
        )

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

        return self.window_resolver.resolve(name)

    # =====================================================
    # FOCUS
    # =====================================================

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

    # =====================================================
    # MINIMIZE
    # =====================================================

    def minimize_window(self, name):
        """Find and minimize a window."""

        window = self.find_window(name)

        if not window:
            return (
                False,
                f"I couldn't find a window called {name}.",
            )

        success = self.window_manager.minimize_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't minimize {window['title']}.",
            )

        return (
            True,
            f"Minimized {window['title']}.",
        )

    # =====================================================
    # MAXIMIZE
    # =====================================================

    def maximize_window(self, name):
        """Find and maximize a window."""

        window = self.find_window(name)

        if not window:
            return (
                False,
                f"I couldn't find a window called {name}.",
            )

        success = self.window_manager.maximize_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't maximize {window['title']}.",
            )

        return (
            True,
            f"Maximized {window['title']}.",
        )

    # =====================================================
    # RESTORE
    # =====================================================

    def restore_window(self, name):
        """Find and restore a window."""

        window = self.find_window(name)

        if not window:
            return (
                False,
                f"I couldn't find a window called {name}.",
            )

        success = self.window_manager.restore_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't restore {window['title']}.",
            )

        return (
            True,
            f"Restored {window['title']}.",
        )

    # =====================================================
    # ACTIVE WINDOW
    # =====================================================

    def minimize_active_window(self):
        """Minimize the currently active window."""

        window = self.active_window()

        if not window:
            return (
                False,
                "I couldn't determine the active window.",
            )

        success = self.window_manager.minimize_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't minimize {window['title']}.",
            )

        return (
            True,
            f"Minimized {window['title']}.",
        )

    def maximize_active_window(self):
        """Maximize the currently active window."""

        window = self.active_window()

        if not window:
            return (
                False,
                "I couldn't determine the active window.",
            )

        success = self.window_manager.maximize_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't maximize {window['title']}.",
            )

        return (
            True,
            f"Maximized {window['title']}.",
        )

    def restore_active_window(self):
        """Restore the currently active window."""

        window = self.active_window()

        if not window:
            return (
                False,
                "I couldn't determine the active window.",
            )

        success = self.window_manager.restore_window(
            window["hwnd"]
        )

        if not success:
            return (
                False,
                f"I couldn't restore {window['title']}.",
            )

        return (
            True,
            f"Restored {window['title']}.",
        )
