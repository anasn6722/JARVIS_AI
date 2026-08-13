import comtypes.client
import win32gui


class UIAutomationController:
    """Windows UI Automation controller using comtypes."""

    CLSID_CUI_AUTOMATION = (
        "{FF48DBA4-60EF-4201-AA87-54103EEF594E}"
    )

    def __init__(self):
        self.UIAutomationCore = (
            comtypes.client.GetModule(
                "UIAutomationCore.dll"
            )
        )

        self.automation = (
            comtypes.client.CreateObject(
                self.CLSID_CUI_AUTOMATION,
                interface=self.UIAutomationCore.IUIAutomation,
            )
        )

    # =========================================================
    # FOREGROUND WINDOW
    # =========================================================

    def foreground_window(self):
        """Return information about the foreground window."""

        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return None

        return {
            "hwnd": hwnd,
            "title": win32gui.GetWindowText(hwnd),
            "class": win32gui.GetClassName(hwnd),
            "rect": win32gui.GetWindowRect(hwnd),
        }

    # =========================================================
    # ELEMENT FROM HANDLE
    # =========================================================

    def element_from_handle(self, hwnd):
        """Return the UI Automation element for an HWND."""

        if not hwnd:
            return None

        return self.automation.ElementFromHandle(
            hwnd
        )

    # =========================================================
    # FOCUSED ELEMENT
    # =========================================================

    def focused_element(self):
        """Return the currently focused UI element."""

        return self.automation.GetFocusedElement()

    # =========================================================
    # ELEMENT FROM POINT
    # =========================================================

    def element_from_point(self, x, y):
        """Return the UI Automation element at screen coordinates."""

        point = self.UIAutomationCore.tagPOINT(
            int(x),
            int(y),
        )

        return self.automation.ElementFromPoint(
            point
        )

    # =========================================================
    # ELEMENT INFO
    # =========================================================

    @staticmethod
    def element_info(element):
        """Return basic semantic information for an element."""

        if element is None:
            return None

        info = {
            "name": "",
            "automation_id": "",
            "class_name": "",
            "control_type": None,
        }

        try:
            info["name"] = element.CurrentName
        except Exception:
            pass

        try:
            info["automation_id"] = (
                element.CurrentAutomationId
            )
        except Exception:
            pass

        try:
            info["class_name"] = (
                element.CurrentClassName
            )
        except Exception:
            pass

        try:
            info["control_type"] = (
                element.CurrentControlType
            )
        except Exception:
            pass

        return info

    # =========================================================
    # ELEMENT RECTANGLE
    # =========================================================

    @staticmethod
    def element_rectangle(element):
        """Return an element's bounding rectangle."""

        if element is None:
            return None

        try:
            rect = element.CurrentBoundingRectangle

            return {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom,
                "width": rect.right - rect.left,
                "height": rect.bottom - rect.top,
            }

        except Exception:
            return None

    # =========================================================
    # INSPECT ELEMENT
    # =========================================================

    def inspect_element(self, element):
        """Return semantic information about one UI element."""

        if element is None:
            return None

        info = self.element_info(
            element
        )

        info["rect"] = self.element_rectangle(
            element
        )

        return info

    # =========================================================
    # INSPECT FOREGROUND
    # =========================================================

    def inspect_foreground(self):
        """
        Inspect the UI Automation element represented by the
        current foreground window.
        """

        window = self.foreground_window()

        if not window:
            return None

        element = self.element_from_handle(
            window["hwnd"]
        )

        if element is None:
            return {
                **window,
                "ui": None,
            }

        return {
            **window,
            "ui": self.inspect_element(
                element
            ),
        }

    # =========================================================
    # INSPECT FOCUSED ELEMENT
    # =========================================================

    def inspect_focused(self):
        """Inspect the currently focused UI element."""

        element = self.focused_element()

        if element is None:
            return None

        return self.inspect_element(
            element
        )

    # =========================================================
    # INSPECT POINT
    # =========================================================

    def inspect_point(self, x, y):
        """Inspect the UI element at screen coordinates."""

        element = self.element_from_point(
            x,
            y,
        )

        if element is None:
            return None

        return self.inspect_element(
            element
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):
        """Release the UI Automation COM object."""

        if getattr(
            self,
            "automation",
            None,
        ) is not None:
            self.automation = None