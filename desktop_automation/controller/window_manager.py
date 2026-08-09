
import win32con
import win32gui


class WindowManager:
    """Controls and inspects visible Windows desktop windows."""

    @staticmethod
    def list_windows():
        """Return visible windows with their handles and titles."""

        windows = []

        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd).strip()

            if not title:
                return

            windows.append(
                {
                    "hwnd": hwnd,
                    "title": title,
                }
            )

        win32gui.EnumWindows(callback, None)

        return windows

    @staticmethod
    def find_window(name):
        """Find a visible window whose title contains name."""

        name = name.lower().strip()

        if not name:
            return None

        for window in WindowManager.list_windows():
            if name in window["title"].lower():
                return window

        return None

    @staticmethod
    def get_active_window():
        """Return the currently active window."""

        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return None

        title = win32gui.GetWindowText(hwnd).strip()

        if not title:
            return None

        return {
            "hwnd": hwnd,
            "title": title,
        }

    @staticmethod
    def focus_window(hwnd):
        """Bring a window to the foreground."""

        if not hwnd:
            return False

        try:
            if not win32gui.IsWindow(hwnd):
                return False

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_RESTORE,
            )

            win32gui.SetForegroundWindow(hwnd)

            return True

        except Exception as error:
            print(
                f"Window focus failed: {error}"
            )

            return False

    @staticmethod
    def minimize_window(hwnd):
        """Minimize a window."""

        if not hwnd:
            return False

        try:
            if not win32gui.IsWindow(hwnd):
                return False

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_MINIMIZE,
            )

            return True

        except Exception as error:
            print(
                f"Window minimize failed: {error}"
            )

            return False

    @staticmethod
    def maximize_window(hwnd):
        """Maximize a window."""

        if not hwnd:
            return False

        try:
            if not win32gui.IsWindow(hwnd):
                return False

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_MAXIMIZE,
            )

            return True

        except Exception as error:
            print(
                f"Window maximize failed: {error}"
            )

            return False

    @staticmethod
    def restore_window(hwnd):
        """Restore a minimized or maximized window."""

        if not hwnd:
            return False

        try:
            if not win32gui.IsWindow(hwnd):
                return False

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_RESTORE,
            )

            return True

        except Exception as error:
            print(
                f"Window restore failed: {error}"
            )

            return False
