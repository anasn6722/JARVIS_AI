from desktop_automation.controller.mouse_controller import (
    MouseController,
)
from desktop_automation.inspector.ui_element_inspector import (
    UIElementInspector,
)


class UIActionController:
    """
    Perform semantic actions on Windows UI Automation elements.

    Strategy:
        1. Prefer the UI Automation Invoke pattern.
        2. Fall back to the element's bounding rectangle.
        3. Use the existing MouseController for the fallback.
    """

    # Windows UI Automation pattern IDs
    UIA_INVOKE_PATTERN_ID = 10000
    UIA_VALUE_PATTERN_ID = 10002
    UIA_SELECTION_ITEM_PATTERN_ID = 10010

    def __init__(
        self,
        inspector=None,
        mouse=None,
    ):
        self.inspector = (
            inspector
            or UIElementInspector()
        )

        self.mouse = (
            mouse
            or MouseController()
        )

        self.automation = (
            self.inspector.controller.automation
        )

    # =========================================================
    # CLICK ELEMENT
    # =========================================================

    def click_element(self, element):
        """
        Click a UI Automation element.
    
        Prefer InvokePattern. Fall back to the element's current
        bounding rectangle and physical mouse click.
        """
    
        if element is None:
            return False, "UI element not found."
    
        # =========================================================
        # INVOKE PATTERN
        # =========================================================
    
        try:
            pattern = element.GetCurrentPattern(
                self.UIA_INVOKE_PATTERN_ID
            )
    
            if pattern is not None:
                pattern.Invoke()
    
                return True, (
                    "UI element invoked successfully."
                )
    
        except Exception:
            pass
        
        # =========================================================
        # RECTANGLE FALLBACK
        # =========================================================
    
        try:
            rect = element.CurrentBoundingRectangle
    
            left = int(rect.left)
            top = int(rect.top)
            right = int(rect.right)
            bottom = int(rect.bottom)
    
        except Exception as error:
            return False, (
                f"Could not read UI element bounds: {error}"
            )
    
        width = right - left
        height = bottom - top
    
        if width <= 0 or height <= 0:
            return False, (
                "UI element has no usable bounding rectangle."
            )
    
        x = left + width // 2
        y = top + height // 2
    
        return self.mouse.left_click(
            x,
            y,
        )

    # =========================================================
    # CLICK BY NAME
    # =========================================================

    def click_by_name(self, name):
        """Find an element by name and click it."""
    
        if not name:
            return False, "A UI element name is required."
    
        element = self.inspector.find_by_name(
            str(name).strip()
        )
    
        if element is None:
            return False, (
                f"UI element not found: {name}"
            )
    
        success, message = self.click_element(
            element
        )
    
        if success:
            try:
                actual_name = (
                    element.CurrentName
                    or name
                )
            except Exception:
                actual_name = name
    
            return True, f"Clicked {actual_name}."
    
        return False, message

    # =========================================================
    # CLICK BY AUTOMATION ID
    # =========================================================

    def click_by_automation_id(
        self,
        automation_id,
    ):
        """Find an element by AutomationId and click it."""

        if not automation_id:
            return (
                False,
                "An AutomationId is required.",
            )

        element = (
            self.inspector.find_by_automation_id(
                automation_id
            )
        )

        if element is None:
            return False, (
                "UI element not found with "
                f"AutomationId: {automation_id}"
            )

        success, message = self.click_element(
            element
        )

        if success:
            return True, (
                "Clicked UI element with "
                f"AutomationId {automation_id}."
            )

        return False, message

    # =========================================================
    # CLICK BY CLASS
    # =========================================================

    def click_by_class(
        self,
        class_name,
    ):
        """Find an element by class name and click it."""

        if not class_name:
            return (
                False,
                "A class name is required.",
            )

        element = self.inspector.find_by_class(
            class_name
        )

        if element is None:
            return False, (
                f"UI element not found with class: "
                f"{class_name}"
            )

        success, message = self.click_element(
            element
        )

        if success:
            return True, (
                f"Clicked element with class "
                f"{class_name}."
            )

        return False, message

    # =========================================================
    # CLICK AT POINT
    # =========================================================

    def click_at_point(
        self,
        x,
        y,
    ):
        """
        Inspect the UI element at a point and click it.

        This gives us a bridge between coordinate-based and
        semantic automation.
        """

        try:
            x = int(x)
            y = int(y)
        except (TypeError, ValueError):
            return (
                False,
                "Coordinates must be integers.",
            )

        element = self.inspector.find_at_point(
            x,
            y,
        )

        if element is None:
            return (
                False,
                f"No UI element found at ({x}, {y}).",
            )

        return self.click_element(
            element
        )

    # =========================================================
    # FOCUS ELEMENT
    # =========================================================

    def focus_element(self, element):
        """
        Focus a UI Automation element.

        Uses SetFocus when available.
        """

        if element is None:
            return False, "UI element not found."

        try:
            element.SetFocus()

            return True, (
                "UI element focused successfully."
            )

        except Exception as error:
            return False, (
                f"Could not focus UI element: {error}"
            )

    # =========================================================
    # FOCUS BY NAME
    # =========================================================

    def focus_by_name(self, name):
        """Find an element by name and focus it."""

        if not name:
            return False, "A UI element name is required."

        element = self.inspector.find_by_name(
            name
        )

        if element is None:
            return False, (
                f"UI element not found: {name}"
            )

        success, message = self.focus_element(
            element
        )

        if success:
            return True, (
                f"Focused {name}."
            )

        return False, message

    # =========================================================
    # FOCUS BY AUTOMATION ID
    # =========================================================

    def focus_by_automation_id(
        self,
        automation_id,
    ):
        """Find an element by AutomationId and focus it."""

        if not automation_id:
            return (
                False,
                "An AutomationId is required.",
            )

        element = (
            self.inspector.find_by_automation_id(
                automation_id
            )
        )

        if element is None:
            return False, (
                "UI element not found with "
                f"AutomationId: {automation_id}"
            )

        return self.focus_element(
            element
        )

    # =========================================================
    # INSPECT BEFORE ACTION
    # =========================================================

    def describe_element(
        self,
        name=None,
        automation_id=None,
        class_name=None,
        control_type=None,
    ):
        """
        Find an element and return its semantic information.

        No action is performed.
        """

        return self.inspector.search_info(
            name=name,
            automation_id=automation_id,
            class_name=class_name,
            control_type=control_type,
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):
        """Release the underlying inspector."""

        if self.inspector is not None:
            self.inspector.close()