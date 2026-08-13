import ctypes
import time
from ctypes import wintypes

# ULONG_PTR is pointer-sized on Windows.
ULONG_PTR = (
    ctypes.c_ulonglong
    if ctypes.sizeof(ctypes.c_void_p) == 8
    else ctypes.c_ulong
)


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUTUNION),
    ]


class KeyboardController:
    """Windows keyboard automation using SendInput."""

    INPUT_KEYBOARD = 1

    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004

    def __init__(self):
        self.user32 = ctypes.WinDLL(
            "user32",
            use_last_error=True,
        )

        self.user32.SendInput.argtypes = [
            wintypes.UINT,
            ctypes.POINTER(INPUT),
            ctypes.c_int,
        ]

        self.user32.SendInput.restype = wintypes.UINT

        self.user32.VkKeyScanW.argtypes = [
            wintypes.WCHAR,
        ]

        self.user32.VkKeyScanW.restype = ctypes.c_short

    # =========================================================
    # LOW LEVEL INPUT
    # =========================================================

    def _send_input(
        self,
        keyboard_input: KEYBDINPUT,
    ) -> None:
        """Send one keyboard INPUT structure."""

        input_data = INPUT(
            type=self.INPUT_KEYBOARD,
            union=INPUTUNION(
                ki=keyboard_input,
            ),
        )

        result = self.user32.SendInput(
            1,
            ctypes.byref(input_data),
            ctypes.sizeof(INPUT),
        )

        if result != 1:
            error_code = ctypes.get_last_error()

            raise OSError(
                error_code,
                f"Windows SendInput failed: "
                f"{ctypes.FormatError(error_code)}",
            )

    # =========================================================
    # KEY PRESS
    # =========================================================

    def _send_key(
        self,
        virtual_key: int,
        flags: int = 0,
    ) -> None:
        """Send a virtual-key event."""

        keyboard_input = KEYBDINPUT(
            wVk=virtual_key,
            wScan=0,
            dwFlags=flags,
            time=0,
            dwExtraInfo=0,
        )

        self._send_input(
            keyboard_input
        )

    def press(
        self,
        key: str,
    ):
        """Press and release a named key."""

        virtual_key = self._virtual_key(key)

        self._send_key(
            virtual_key
        )

        self._send_key(
            virtual_key,
            self.KEYEVENTF_KEYUP,
        )

        return True, f"Pressed {key}."

    # =========================================================
    # HOTKEY
    # =========================================================

    def hotkey(
        self,
        *keys: str,
    ):
        """Press a combination such as Ctrl+C."""

        if not keys:
            return False, "No keys provided."

        virtual_keys = [
            self._virtual_key(key)
            for key in keys
        ]

        try:
            for virtual_key in virtual_keys:
                self._send_key(
                    virtual_key
                )

        finally:
            for virtual_key in reversed(
                virtual_keys
            ):
                self._send_key(
                    virtual_key,
                    self.KEYEVENTF_KEYUP,
                )

        return (
            True,
            "Pressed "
            + " + ".join(keys)
            + ".",
        )

    # =========================================================
    # TYPE TEXT
    # =========================================================

    def type_text(
        self,
        text: str,
        interval: float = 0.01,
    ):
        """Type Unicode text using KEYEVENTF_UNICODE."""

        if not text:
            return False, "No text provided."

        for character in text:
            code_point = ord(character)

            # KEY DOWN
            key_down = KEYBDINPUT(
                wVk=0,
                wScan=code_point,
                dwFlags=self.KEYEVENTF_UNICODE,
                time=0,
                dwExtraInfo=0,
            )

            self._send_input(
                key_down
            )

            # KEY UP
            key_up = KEYBDINPUT(
                wVk=0,
                wScan=code_point,
                dwFlags=(
                    self.KEYEVENTF_UNICODE
                    | self.KEYEVENTF_KEYUP
                ),
                time=0,
                dwExtraInfo=0,
            )

            self._send_input(
                key_up
            )

            if interval:
                time.sleep(interval)

        return True, f"Typed {text!r}."

    # =========================================================
    # KEY RESOLUTION
    # =========================================================

    
    def _virtual_key(
        self,
        key: str,
    ) -> int:
        """Convert a human-readable key name to a VK code."""

        normalized = key.strip().lower()

        key_map = {
            "enter": 0x0D,
            "return": 0x0D,
            "tab": 0x09,
            "escape": 0x1B,
            "esc": 0x1B,
            "backspace": 0x08,
            "delete": 0x2E,
            "del": 0x2E,
            "space": 0x20,
            "up": 0x26,
            "down": 0x28,
            "left": 0x25,
            "right": 0x27,
            "home": 0x24,
            "end": 0x23,
            "pageup": 0x21,
            "pagedown": 0x22,
            "shift": 0x10,
            "ctrl": 0x11,
            "control": 0x11,
            "alt": 0x12,
            "windows": 0x5B,
            "win": 0x5B,
            "capslock": 0x14,
            "insert": 0x2D,
            "f1": 0x70,
            "f2": 0x71,
            "f3": 0x72,
            "f4": 0x73,
            "f5": 0x74,
            "f6": 0x75,
            "f7": 0x76,
            "f8": 0x77,
            "f9": 0x78,
            "f10": 0x79,
            "f11": 0x7A,
            "f12": 0x7B,
        }

        if normalized in key_map:
            return key_map[normalized]

        if len(normalized) == 1:
            vk = self.user32.VkKeyScanW(
                normalized
            )

            if vk == -1:
                raise ValueError(
                    f"Unsupported key: {key}"
                )

            return vk & 0xFF

        raise ValueError(
            f"Unsupported key: {key}"
        )