
import win32con
import win32gui


class WindowManager:
    """Controls and inspects visible Windows desktop windows."""

    @staticmethod
    def list_windows():
        """Return visible windows with their titles and handles."""

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
        """Find a visible window whose title contains the given name."""

        name = name.lower().strip()

        for window in WindowManager.list_windows():
            if name in window["title"].lower():
                return window

        return None

    @staticmethod
    def get_active_window():
        """Return information about the currently active window."""

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

        try:
            win32gui.ShowWindow(
                hwnd,
                win32con.SW_RESTORE,
            )

            win32gui.SetForegroundWindow(hwnd)

            return True

        except Exception:
            return False

    @staticmethod
    def close_window(hwnd):
        """Request a window to close."""

        try:
            win32gui.PostMessage(
                hwnd,
                win32con.WM_CLOSE,
                0,
                0,
            )

            return True

        except Exception:
            return False
