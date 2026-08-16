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
from desktop_automation.resolver.ui_target_resolver import (
    UITargetResolver,
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

        self.ui_target_resolver = UITargetResolver()

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
            Explorer
            Toggle Chat
        """

        if not target:
            return False, "A UI element name is required."

        target = str(target).strip()

        resolved = self.ui_target_resolver.resolve(
            target
        )

        if resolved is None:
            return False, (
                f"Could not resolve UI target: {target}"
            )

        # Capability-based Search.
        if resolved.capability == "search_ui":
            info = self.ui_inspector.search_info(
                name="Search (Ctrl+Shift+F)"
            )

            if info is not None:
                return True, info

            return False, "Search UI element not found."

        # Capability-based Explorer.
        if resolved.capability == "explorer_ui":
            info = self.ui_inspector.search_info(
                name="Explorer (Ctrl+Shift+E)"
            )

            if info is not None:
                return True, info

            return False, "Explorer UI element not found."

        info = self.ui_inspector.search_info(
            name=resolved.target
        )

        if info is None:
            return (
                False,
                f"UI element not found: {resolved.target}",
            )

        return True, info

    def ui_find_descriptor(self, target):
        """
        Find a UI target and return a semantic descriptor.

        Capability-based targets are represented by a stable
        descriptor even when their visible UI Automation element
        is temporarily unavailable.
        """

        if not target:
            return False, "A UI element name is required."

        target = str(target).strip()

        resolved = self.ui_target_resolver.resolve(
            target
        )

        if resolved is None:
            return False, (
                f"Could not resolve UI target: {target}"
            )

        # =====================================================
        # SEARCH CAPABILITY
        # =====================================================

        if resolved.capability == "search_ui":
            info = self.ui_inspector.search_info(
                name="Search (Ctrl+Shift+F)"
            )

            if info is not None:
                info["capability"] = "search_ui"
                info["semantic_target"] = "Search"

                return True, info

            return True, {
                "name": "Search",
                "automation_id": "",
                "class_name": "",
                "control_type": None,
                "capability": "search_ui",
                "semantic_target": "Search",
            }

        # =====================================================
        # EXPLORER CAPABILITY
        # =====================================================

        if resolved.capability == "explorer_ui":
            info = self.ui_inspector.search_info(
                name="Explorer (Ctrl+Shift+E)"
            )

            if info is not None:
                info["capability"] = "explorer_ui"
                info["semantic_target"] = "Explorer"

                return True, info

            return True, {
                "name": "Explorer",
                "automation_id": "",
                "class_name": "",
                "control_type": None,
                "capability": "explorer_ui",
                "semantic_target": "Explorer",
            }

        # =====================================================
        # NORMAL UI TARGET
        # =====================================================

        info = self.ui_inspector.search_info(
            name=resolved.target
        )

        if info is None:
            return (
                False,
                f"UI element not found: {resolved.target}",
            )

        info["semantic_target"] = resolved.target

        return True, info

    def ui_click_descriptor(self, descriptor):
        """
        Re-resolve a previously discovered UI descriptor
        and click it.

        Capability-based descriptors can execute stable
        keyboard shortcuts when the visible UI Automation
        element is unavailable.
        """

        if not isinstance(descriptor, dict):
            return (
                False,
                "UI descriptor must be a dictionary.",
            )

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        # =====================================================
        # SEARCH CAPABILITY
        # =====================================================

        if capability == "search_ui":
            return self.keyboard.hotkey(
                "ctrl",
                "shift",
                "f",
            )

        # =====================================================
        # EXPLORER CAPABILITY
        # =====================================================

        if capability == "explorer_ui":
            return self.keyboard.hotkey(
                "ctrl",
                "shift",
                "e",
            )

        name = str(
            descriptor.get("name") or ""
        ).strip()

        automation_id = str(
            descriptor.get("automation_id") or ""
        ).strip()

        class_name = str(
            descriptor.get("class_name") or ""
        ).strip()

        control_type = descriptor.get(
            "control_type"
        )

        element = None

        # =====================================================
        # PREFER AUTOMATION ID
        # =====================================================

        if automation_id:
            element = (
                self.ui_inspector.find_by_automation_id(
                    automation_id
                )
            )

        # =====================================================
        # FALLBACK: NAME
        # =====================================================

        if element is None and name:
            element = (
                self.ui_inspector.find_by_name(
                    name
                )
            )

        # =====================================================
        # FALLBACK: CLASS
        # =====================================================

        if element is None and class_name:
            element = (
                self.ui_inspector.find_by_class(
                    class_name
                )
            )

        # =====================================================
        # FALLBACK: CONTROL TYPE
        # =====================================================

        if (
            element is None
            and control_type is not None
        ):
            element = (
                self.ui_inspector.find_by_control_type(
                    control_type
                )
            )

        if element is None:
            return (
                False,
                "UI element could not be re-resolved.",
            )

        return self.ui_actions.click_element(
            element
        )

    def ui_type_descriptor(self, payload):
        """
        Re-resolve a semantic UI descriptor and type text into it.

        Expected payload:

            {
                "descriptor": {
                    "name": "Search",
                    ...
                },
                "text": "Python"
            }
        """

        if not isinstance(payload, dict):
            return (
                False,
                "UI typing payload must be a dictionary.",
            )

        descriptor = payload.get(
            "descriptor"
        )

        text = payload.get(
            "text"
        )

        if not isinstance(descriptor, dict):
            return (
                False,
                "UI descriptor is required.",
            )

        if text is None:
            return False, "Text is required."

        text = str(text)

        if not text:
            return False, "Text is empty."

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        # =====================================================
        # SEARCH CAPABILITY
        # =====================================================

        if capability == "search_ui":
            return self.ui_actions.type_into_search_action(
                text
            )

        name = str(
            descriptor.get("name") or ""
        ).strip()

        automation_id = str(
            descriptor.get("automation_id") or ""
        ).strip()

        class_name = str(
            descriptor.get("class_name") or ""
        ).strip()

        control_type = descriptor.get(
            "control_type"
        )

        element = None

        # =====================================================
        # PREFER AUTOMATION ID
        # =====================================================

        if automation_id:
            element = (
                self.ui_inspector.find_by_automation_id(
                    automation_id
                )
            )

        # =====================================================
        # FALLBACK: NAME
        # =====================================================

        if element is None and name:
            element = (
                self.ui_inspector.find_by_name(
                    name
                )
            )

        # =====================================================
        # FALLBACK: CLASS
        # =====================================================

        if element is None and class_name:
            element = (
                self.ui_inspector.find_by_class(
                    class_name
                )
            )

        # =====================================================
        # FALLBACK: CONTROL TYPE
        # =====================================================

        if (
            element is None
            and control_type is not None
        ):
            element = (
                self.ui_inspector.find_by_control_type(
                    control_type
                )
            )

        if element is None:
            return (
                False,
                "UI element could not be re-resolved.",
            )

        return self.ui_actions.type_into_element(
            element,
            text,
        )

    def ui_click(self, target):
        """Find and click a semantic UI target."""

        if not target:
            return False, "A UI element name is required."

        resolved = self.ui_target_resolver.resolve(
            target
        )

        if resolved is None:
            return False, (
                f"Could not resolve UI target: {target}"
            )

        # =====================================================
        # SEARCH CAPABILITY
        # =====================================================

        if resolved.capability == "search_ui":
            return self.keyboard.hotkey(
                "ctrl",
                "shift",
                "f",
            )

        # =====================================================
        # EXPLORER CAPABILITY
        # =====================================================

        if resolved.capability == "explorer_ui":
            return self.keyboard.hotkey(
                "ctrl",
                "shift",
                "e",
            )

        return self.ui_actions.click_by_name(
            resolved.target
        )

    def ui_focus(self, target):
        """Find and focus a semantic UI target."""

        if not target:
            return False, "A UI element name is required."

        resolved = self.ui_target_resolver.resolve(
            target
        )

        if resolved is None:
            return False, (
                f"Could not resolve UI target: {target}"
            )

        # =====================================================
        # SEARCH CAPABILITY
        # =====================================================

        if resolved.capability == "search_ui":
            success, message = self.keyboard.hotkey(
                "ctrl",
                "shift",
                "f",
            )

            if success:
                return True, "Focused Search."

            return False, message

        # =====================================================
        # EXPLORER CAPABILITY
        # =====================================================

        if resolved.capability == "explorer_ui":
            success, message = self.keyboard.hotkey(
                "ctrl",
                "shift",
                "e",
            )

            if success:
                return True, "Focused Explorer."

            return False, message

        return self.ui_actions.focus_by_name(
            resolved.target
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

    # =========================================================
    # UI TYPE
    # =========================================================

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
            return (
                False,
                "UI element name is required.",
            )

        if not text:
            return False, "Text is empty."

        resolved = self.ui_target_resolver.resolve(
            element_name
        )

        if resolved is None:
            return False, (
                f"Could not resolve UI target: "
                f"{element_name}"
            )

        if resolved.capability == "search_ui":
            return self.ui_actions.type_into_search_action(
                text
            )

        return self.ui_actions.type_into_name(
            resolved.target,
            text,
        )

    # =========================================================
    # SEARCH UI
    # =========================================================

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

        # =====================================================
        # OPEN SEARCH
        # =====================================================

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

        # =====================================================
        # VERIFY FOCUSED ELEMENT
        # =====================================================

        focused = (
            self.ui_inspector.controller.focused_element()
        )

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

        # =====================================================
        # TYPE QUERY
        # =====================================================

        success, message = self.keyboard.type_text(
            query
        )

        if not success:
            return False, (
                f"Could not type search query: {message}"
            )

        # =====================================================
        # SUBMIT SEARCH
        # =====================================================

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