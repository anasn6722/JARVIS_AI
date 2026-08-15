from desktop_automation.actions.ui_action_controller import (
    UIActionController,
)
from desktop_automation.controller.keyboard_controller import (
    KeyboardController,
)
from desktop_automation.controller.mouse_controller import (
    MouseController,
)
from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.inspector.ui_element_inspector import (
    UIElementInspector,
)
from desktop_automation.resolver.window_resolver import WindowResolver


class DesktopController:
    """High-level controller for Windows desktop automation."""

    def __init__(self):
        self.window_manager = WindowManager()
        self.window_resolver = WindowResolver(
            self.window_manager
        )

        self.mouse = MouseController()
        self.keyboard = KeyboardController()

        # =====================================================
        # SEMANTIC UI AUTOMATION
        # =====================================================

        self.ui_inspector = UIElementInspector()

        self.ui_actions = UIActionController(
            inspector=self.ui_inspector,
            mouse=self.mouse,
        )

    # =========================================================
    # WINDOWS
    # =========================================================

    def list_windows(self):
        """Return all visible desktop windows."""

        return self.window_manager.list_windows()

    def get_active_window(self):
        """Return the currently active window."""

        return self.window_manager.get_active_window()

    def minimize_active_window(self):
        """Minimize the currently active window."""

        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.minimize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Minimized {window['title']}."

        return (
            False,
            f"Could not minimize {window['title']}.",
        )

    def maximize_active_window(self):
        """Maximize the currently active window."""

        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.maximize_window(
            window["hwnd"]
        )

        if success:
            return True, f"Maximized {window['title']}."

        return (
            False,
            f"Could not maximize {window['title']}.",
        )

    def restore_active_window(self):
        """Restore the currently active window."""

        window = self.window_manager.get_active_window()

        if not window:
            return False, "No active window found."

        success = self.window_manager.restore_window(
            window["hwnd"]
        )

        if success:
            return True, f"Restored {window['title']}."

        return (
            False,
            f"Could not restore {window['title']}.",
        )

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

        return (
            False,
            f"Could not close {window['title']}.",
        )

    def focus_window(self, name):
        """Find and focus a desktop window."""

        window = self.window_resolver.resolve(name)

        if not window:
            return False, f"Window not found: {name}"

        success = self.window_manager.focus_window(
            window["hwnd"]
        )

        if success:
            return True, f"Focused {window['title']}."

        return (
            False,
            f"Could not focus {window['title']}.",
        )

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

        return (
            False,
            f"Could not minimize {window['title']}.",
        )

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

        return (
            False,
            f"Could not maximize {window['title']}.",
        )

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

        return (
            False,
            f"Could not restore {window['title']}.",
        )

    # =========================================================
    # MOUSE
    # =========================================================

    def mouse_position(self):
        """Return the current mouse position."""

        x, y = self.mouse.position()

        return (
            True,
            f"Mouse position: ({x}, {y}).",
        )

    def mouse_move(self, target):
        """Move the mouse using x,y coordinates."""

        try:
            x, y = self._parse_coordinates(target)

            return self.mouse.move(x, y)

        except (TypeError, ValueError) as error:
            return False, str(error)

    def mouse_click(self, target=None):
        """Left-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)

                return self.mouse.left_click(
                    x,
                    y,
                )

            return self.mouse.left_click()

        except (TypeError, ValueError) as error:
            return False, str(error)

    def mouse_double_click(self, target=None):
        """Double-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)

                return self.mouse.double_click(
                    x,
                    y,
                )

            return self.mouse.double_click()

        except (TypeError, ValueError) as error:
            return False, str(error)

    def mouse_right_click(self, target=None):
        """Right-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)

                return self.mouse.right_click(
                    x,
                    y,
                )

            return self.mouse.right_click()

        except (TypeError, ValueError) as error:
            return False, str(error)

    def mouse_middle_click(self, target=None):
        """Middle-click at coordinates or current position."""

        try:
            if target:
                x, y = self._parse_coordinates(target)

                return self.mouse.middle_click(
                    x,
                    y,
                )

            return self.mouse.middle_click()

        except (TypeError, ValueError) as error:
            return False, str(error)

    def mouse_scroll(self, target):
        """Scroll using a positive or negative integer."""

        try:
            amount = int(
                str(target).strip()
            )

        except (TypeError, ValueError):
            return (
                False,
                "Scroll amount must be an integer.",
            )

        return self.mouse.scroll(amount)

    # =========================================================
    # KEYBOARD
    # =========================================================

    def keyboard_type(self, text):
        """Type text into the currently focused application."""

        if text is None:
            return False, "Text is required."

        text = str(text)

        if not text:
            return False, "Text is empty."

        try:
            return self.keyboard.type_text(
                text
            )

        except (TypeError, ValueError, OSError) as error:
            return False, str(error)

    def keyboard_press(self, key):
        """Press and release a single keyboard key."""

        if not key:
            return False, "A key is required."

        try:
            return self.keyboard.press(
                str(key).strip()
            )

        except (TypeError, ValueError, OSError) as error:
            return False, str(error)

    def keyboard_hotkey(self, keys):
        """
        Press a keyboard combination.

        Examples:
            ctrl+a
            ctrl+c
            ctrl+v
            alt+tab
        """

        if not keys:
            return False, "Keys are required."

        if isinstance(keys, str):
            normalized = (
                keys
                .replace(",", "+")
                .strip()
            )

            parts = [
                part.strip()
                for part in normalized.split("+")
                if part.strip()
            ]

        elif isinstance(keys, (list, tuple)):
            parts = [
                str(part).strip()
                for part in keys
                if str(part).strip()
            ]

        else:
            return (
                False,
                "Keys must be a string or list.",
            )

        if not parts:
            return False, "No keys provided."

        try:
            return self.keyboard.hotkey(
                *parts
            )

        except (
            TypeError,
            ValueError,
            OSError,
        ) as error:
            return False, str(error)

    # =========================================================
    # SEMANTIC UI
    # =========================================================

    def ui_find(self, target):
        """
        Find a UI element by its visible semantic name.

        Example:
            File
            Explorer (Ctrl+Shift+E)
            Toggle Chat
        """

        if not target:
            return False, "A UI element name is required."

        info = self.ui_inspector.search_info(
            name=str(target).strip()
        )

        if info is None:
            return (
                False,
                f"UI element not found: {target}",
            )

        return (
            True,
            info,
        )

    def ui_click(self, target):
        """
        Find a UI element by name and click it.

        Example:
            ui_click("File")
        """

        if not target:
            return False, "A UI element name is required."

        return self.ui_actions.click_by_name(
            str(target).strip()
        )

    def ui_focus(self, target):
        """
        Find a UI element by name and focus it.

        Example:
            ui_focus("Agent Status")
        """

        if not target:
            return False, "A UI element name is required."

        return self.ui_actions.focus_by_name(
            str(target).strip()
        )

    def ui_click_at(self, target):
        """
        Inspect the UI element at x,y and click it.

        Example:
            ui_click_at("500,300")
        """

        try:
            x, y = self._parse_coordinates(
                target
            )

        except (TypeError, ValueError) as error:
            return False, str(error)

        return self.ui_actions.click_at_point(
            x,
            y,
        )

    def ui_describe(self, target):
        """
        Find a UI element by name and return its metadata.
        """

        if not target:
            return False, "A UI element name is required."

        info = self.ui_actions.describe_element(
            name=str(target).strip()
        )

        if info is None:
            return (
                False,
                f"UI element not found: {target}",
            )

        return True, info

    # =========================================================
    # PARSING
    # =========================================================

    @staticmethod
    def _parse_coordinates(target):
        """Parse coordinates from 'x,y'."""

        if not isinstance(target, str):
            raise ValueError(
                "Coordinates must be provided as 'x,y'."
            )

        parts = [
            part.strip()
            for part in target.split(",")
        ]

        if len(parts) != 2:
            raise ValueError(
                "Coordinates must use the format 'x,y'."
            )

        try:
            x = int(parts[0])
            y = int(parts[1])

        except ValueError as error:
            raise ValueError(
                "Coordinates must be integers."
            ) from error

        return x, y

    def ui_type(self, target):
        """
        Type into a semantic UI target.

        Supported:
            Search||text
            exact UI element||text
        """

        if not target:
            return False, "UI typing target is required."

        if "||" not in target:
            return (
                False,
                "UI typing target must use: element||text",
            )

        element_name, text = target.split(
            "||",
            1,
        )

        element_name = element_name.strip()
        text = text.strip()

        if not element_name:
            return False, "UI element name is required."

        if not text:
            return False, "Text is required."

        # =========================================================
        # SPECIALIZED SEARCH ACTION
        # =========================================================

        if element_name.lower() in {
            "search",
            "search box",
            "search panel",
        }:
            return self.ui_actions.type_into_search_action(
                text
            )

        # =========================================================
        # GENERIC UI ELEMENT
        # =========================================================

        return self.ui_actions.type_into_name(
            element_name,
            text,
        )

    def search_ui(self, query):
        """
        Open the application's Search interface, type the query,
        and submit it.
    
        VS Code exposes Search through Ctrl+Shift+F, which is more
        reliable than depending on a changing UI element name.
        """
    
        if query is None:
            return False, "Search query is required."
    
        query = str(query).strip()
    
        if not query:
            return False, "Search query is empty."
    
        # =========================================================
        # OPEN SEARCH
        # =========================================================
    
        success, message = self.keyboard.hotkey(
            "ctrl",
            "shift",
            "f",
        )
    
        if not success:
            return False, (
                f"Could not open Search: {message}"
            )
    
        # Give the application time to update its UI.
        import time
    
        time.sleep(0.2)
    
        # =========================================================
        # VERIFY FOCUSED ELEMENT
        # =========================================================
    
        focused = self.ui_inspector.controller.focused_element()
    
        if focused is None:
            return (
                False,
                "Search opened, but no focused input was found.",
            )
    
        try:
            focused_name = (
                focused.CurrentName or ""
            )
    
            focused_class = (
                focused.CurrentClassName or ""
            )
    
        except Exception:
            focused_name = ""
            focused_class = ""
    
        print(
            "Focused after Search:",
            focused_name,
            focused_class,
        )
    
        # =========================================================
        # TYPE QUERY
        # =========================================================
    
        success, message = self.keyboard.type_text(
            query
        )
    
        if not success:
            return False, (
                f"Could not type search query: {message}"
            )
    
        # =========================================================
        # SUBMIT SEARCH
        # =========================================================
    
        success, message = self.keyboard.press(
            "enter"
        )
    
        if not success:
            return False, (
                f"Could not submit search: {message}"
            )
    
        return True, (
            f"Searched for '{query}'."
        )
    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):
        """Release UI automation resources."""

        if self.ui_inspector is not None:
            self.ui_inspector.close()