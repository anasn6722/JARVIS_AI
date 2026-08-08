
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
    def close_window(hwnd):
        """Request a specific window to close."""

        if not hwnd:
            return False

        try:
            if not win32gui.IsWindow(hwnd):
                return False

            win32gui.PostMessage(
                hwnd,
                win32con.WM_CLOSE,
                0,
                0,
            )

            return True

        except Exception as error:
            print(
                f"Window close failed: {error}"
            )

            return False
