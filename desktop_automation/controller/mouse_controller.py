import ctypes
import time
from ctypes import wintypes


class MouseController:
    """Low-level Windows mouse controller."""

    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010

    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040

    MOUSEEVENTF_WHEEL = 0x0800

    def __init__(self):
        self.user32 = ctypes.windll.user32

    # =========================================================
    # SCREEN
    # =========================================================

    def screen_size(self) -> tuple[int, int]:
        """Return screen width and height."""

        width = self.user32.GetSystemMetrics(0)
        height = self.user32.GetSystemMetrics(1)

        return width, height

    def position(self) -> tuple[int, int]:
        """Return the current cursor position."""

        point = wintypes.POINT()

        if not self.user32.GetCursorPos(
            ctypes.byref(point)
        ):
            raise OSError("Could not get cursor position.")

        return point.x, point.y

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_coordinates(
        self,
        x: int,
        y: int,
    ) -> None:
        """Validate coordinates against the primary screen."""

        width, height = self.screen_size()

        if not 0 <= x < width:
            raise ValueError(
                f"X coordinate must be between 0 and {width - 1}."
            )

        if not 0 <= y < height:
            raise ValueError(
                f"Y coordinate must be between 0 and {height - 1}."
            )

    # =========================================================
    # MOVE
    # =========================================================

    def move(
        self,
        x: int,
        y: int,
    ) -> tuple[bool, str]:
        """Move the cursor to an absolute screen position."""

        self._validate_coordinates(x, y)

        success = self.user32.SetCursorPos(
            x,
            y,
        )

        if not success:
            return (
                False,
                f"Could not move mouse to ({x}, {y}).",
            )

        return (
            True,
            f"Moved mouse to ({x}, {y}).",
        )

    # =========================================================
    # LEFT CLICK
    # =========================================================

    def left_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> tuple[bool, str]:
        """Perform a left click."""

        if x is not None and y is not None:
            self._validate_coordinates(x, y)

            if not self.user32.SetCursorPos(x, y):
                return (
                    False,
                    f"Could not move mouse to ({x}, {y}).",
                )

        self.user32.mouse_event(
            self.MOUSEEVENTF_LEFTDOWN,
            0,
            0,
            0,
            0,
        )

        self.user32.mouse_event(
            self.MOUSEEVENTF_LEFTUP,
            0,
            0,
            0,
            0,
        )

        if x is not None and y is not None:
            return (
                True,
                f"Clicked at ({x}, {y}).",
            )

        return (
            True,
            "Left click completed.",
        )

    # =========================================================
    # DOUBLE CLICK
    # =========================================================

    def double_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> tuple[bool, str]:
        """Perform a double left click."""

        first = self.left_click(x, y)

        if not first[0]:
            return first

        time.sleep(0.08)

        second = self.left_click()

        if not second[0]:
            return second

        if x is not None and y is not None:
            return (
                True,
                f"Double-clicked at ({x}, {y}).",
            )

        return (
            True,
            "Double click completed.",
        )

    # =========================================================
    # RIGHT CLICK
    # =========================================================

    def right_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> tuple[bool, str]:
        """Perform a right click."""

        if x is not None and y is not None:
            self._validate_coordinates(x, y)

            if not self.user32.SetCursorPos(x, y):
                return (
                    False,
                    f"Could not move mouse to ({x}, {y}).",
                )

        self.user32.mouse_event(
            self.MOUSEEVENTF_RIGHTDOWN,
            0,
            0,
            0,
            0,
        )

        self.user32.mouse_event(
            self.MOUSEEVENTF_RIGHTUP,
            0,
            0,
            0,
            0,
        )

        if x is not None and y is not None:
            return (
                True,
                f"Right-clicked at ({x}, {y}).",
            )

        return (
            True,
            "Right click completed.",
        )

    # =========================================================
    # MIDDLE CLICK
    # =========================================================

    def middle_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> tuple[bool, str]:
        """Perform a middle click."""

        if x is not None and y is not None:
            self._validate_coordinates(x, y)

            if not self.user32.SetCursorPos(x, y):
                return (
                    False,
                    f"Could not move mouse to ({x}, {y}).",
                )

        self.user32.mouse_event(
            self.MOUSEEVENTF_MIDDLEDOWN,
            0,
            0,
            0,
            0,
        )

        self.user32.mouse_event(
            self.MOUSEEVENTF_MIDDLEUP,
            0,
            0,
            0,
            0,
        )

        if x is not None and y is not None:
            return (
                True,
                f"Middle-clicked at ({x}, {y}).",
            )

        return (
            True,
            "Middle click completed.",
        )

    # =========================================================
    # SCROLL
    # =========================================================

    def scroll(
        self,
        amount: int,
    ) -> tuple[bool, str]:
        """Scroll vertically.

        Positive values scroll up.
        Negative values scroll down.
        """

        if amount == 0:
            return (
                False,
                "Scroll amount cannot be zero.",
            )

        self.user32.mouse_event(
            self.MOUSEEVENTF_WHEEL,
            0,
            0,
            int(amount * 120),
            0,
        )

        direction = (
            "up"
            if amount > 0
            else "down"
        )

        return (
            True,
            f"Scrolled {direction} {abs(amount)} step(s).",
        )