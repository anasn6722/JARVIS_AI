import ctypes
from ctypes import wintypes

import win32gui


class UIAutomationController:
    """Low-level Windows UI Automation foundation."""

    CLSID_CUI_AUTOMATION = (
        "{FF48DBA4-60EF-4201-AA87-54103EEF594E}"
    )

    IID_IUI_AUTOMATION = (
        "{30CBE57D-D9D0-452A-AB13-7AC5AC4825EE}"
    )

    COINIT_APARTMENTTHREADED = 0x2

    def __init__(self):
        self.ole32 = ctypes.WinDLL(
            "ole32",
            use_last_error=True,
        )

        self._initialize_com()

        self.automation = self._create_automation()

    # =========================================================
    # COM
    # =========================================================

    def _initialize_com(self):
        """Initialize COM for the current thread."""

        result = self.ole32.CoInitializeEx(
            None,
            self.COINIT_APARTMENTTHREADED,
        )

        # S_OK = 0
        # S_FALSE = 1
        # RPC_E_CHANGED_MODE = 0x80010106
        if result not in (0, 1):
            raise OSError(
                result,
                "CoInitializeEx failed.",
            )

    def _create_automation(self):
        """
        Create the native CUIAutomation COM object.

        The ProgID approach is intentionally avoided because
        CUIAutomation8.CUIAutomation8 was unavailable on this system.
        """

        clsid = ctypes.c_buffer(
            16
        )

        iid = ctypes.c_buffer(
            16
        )

        if (
            self.ole32.CLSIDFromString(
                self.CLSID_CUI_AUTOMATION,
                clsid,
            )
            != 0
        ):
            raise OSError(
                "CLSIDFromString failed."
            )

        if (
            self.ole32.CLSIDFromString(
                self.IID_IUI_AUTOMATION,
                iid,
            )
            != 0
        ):
            raise OSError(
                "IID conversion failed."
            )

        interface = ctypes.c_void_p()

        result = self.ole32.CoCreateInstance(
            clsid,
            None,
            1,
            iid,
            ctypes.byref(interface),
        )

        if result != 0:
            raise OSError(
                result,
                "CoCreateInstance failed.",
            )

        return interface

    # =========================================================
    # FOREGROUND WINDOW
    # =========================================================

    def foreground_window(self):
        """Return foreground window metadata."""

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
    # CLOSE
    # =========================================================

    def close(self):
        """Release COM resources."""

        if getattr(self, "automation", None):
            # Final COM release will be handled later when we expose
            # the actual IUIAutomation vtable methods.
            self.automation = None

        self.ole32.CoUninitialize()