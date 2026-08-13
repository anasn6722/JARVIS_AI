from comtypes.automation import VARIANT

from desktop_automation.controller.ui_automation_controller import (
    UIAutomationController,
)


class UIElementInspector:
    """
    High-level semantic UI element search.

    Uses Windows UI Automation through UIAutomationController.
    """

    # =========================================================
    # UI AUTOMATION CONSTANTS
    # =========================================================

    TREE_SCOPE_ELEMENT = 0x1
    TREE_SCOPE_CHILDREN = 0x2
    TREE_SCOPE_DESCENDANTS = 0x4

    # UI Automation property IDs
    UIA_NAME_PROPERTY_ID = 30005
    UIA_AUTOMATION_ID_PROPERTY_ID = 30011
    UIA_CLASSNAME_PROPERTY_ID = 30012
    UIA_CONTROLTYPE_PROPERTY_ID = 30003

    def __init__(
        self,
        controller=None,
    ):
        self.controller = (
            controller
            or UIAutomationController()
        )

    # =========================================================
    # CURRENT WINDOW
    # =========================================================

    def current_window(self):
        """Return the current foreground window."""

        return self.controller.foreground_window()

    # =========================================================
    # CURRENT ELEMENT
    # =========================================================

    def current_element(self):
        """
        Return the UI Automation element representing the
        current foreground window.
        """

        window = self.current_window()

        if not window:
            return None

        return self.controller.element_from_handle(
            window["hwnd"]
        )

    # =========================================================
    # ELEMENT INFO
    # =========================================================

    def inspect(self, element):
        """Convert an automation element into readable metadata."""

        if element is None:
            return None

        return self.controller.inspect_element(
            element
        )

    # =========================================================
    # FIND BY NAME
    # =========================================================

    def find_by_name(
        self,
        name,
        root=None,
        descendants=True,
    ):
        """
        Find the first element whose Name matches `name`.
        """

        if not name:
            return None

        root = root or self.current_element()

        if root is None:
            return None

        condition = (
            self.controller.automation.CreatePropertyCondition(
                self.UIA_NAME_PROPERTY_ID,
                VARIANT(str(name)),
            )
        )

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        element = root.FindFirst(
            scope,
            condition,
        )

        return element

    # =========================================================
    # FIND BY AUTOMATION ID
    # =========================================================

    def find_by_automation_id(
        self,
        automation_id,
        root=None,
        descendants=True,
    ):
        """Find the first element by AutomationId."""

        if not automation_id:
            return None

        root = root or self.current_element()

        if root is None:
            return None

        condition = (
            self.controller.automation.CreatePropertyCondition(
                self.UIA_AUTOMATION_ID_PROPERTY_ID,
                VARIANT(str(automation_id)),
            )
        )

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        return root.FindFirst(
            scope,
            condition,
        )

    # =========================================================
    # FIND BY CLASS NAME
    # =========================================================

    def find_by_class(
        self,
        class_name,
        root=None,
        descendants=True,
    ):
        """Find the first element by ClassName."""

        if not class_name:
            return None

        root = root or self.current_element()

        if root is None:
            return None

        condition = (
            self.controller.automation.CreatePropertyCondition(
                self.UIA_CLASSNAME_PROPERTY_ID,
                VARIANT(str(class_name)),
            )
        )

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        return root.FindFirst(
            scope,
            condition,
        )

    # =========================================================
    # FIND BY CONTROL TYPE
    # =========================================================

    def find_by_control_type(
        self,
        control_type,
        root=None,
        descendants=True,
    ):
        """
        Find the first element by UI Automation ControlType.

        Example:
            50000 = Button
            50020 = Edit
        """

        root = root or self.current_element()

        if root is None:
            return None

        try:
            control_type = int(
                control_type
            )
        except (TypeError, ValueError):
            return None

        condition = (
            self.controller.automation.CreatePropertyCondition(
                self.UIA_CONTROLTYPE_PROPERTY_ID,
                VARIANT(control_type),
            )
        )

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        return root.FindFirst(
            scope,
            condition,
        )

    # =========================================================
    # FIND AT POINT
    # =========================================================

    def find_at_point(
        self,
        x,
        y,
    ):
        """Find the UI element at screen coordinates."""

        element = self.controller.element_from_point(
            int(x),
            int(y),
        )

        if element is None:
            return None

        return element

    # =========================================================
    # INSPECT AT POINT
    # =========================================================

    def inspect_at_point(
        self,
        x,
        y,
    ):
        """Inspect the UI element at screen coordinates."""

        element = self.find_at_point(
            x,
            y,
        )

        if element is None:
            return None

        return self.inspect(
            element
        )

    # =========================================================
    # FIND ALL DESCENDANTS
    # =========================================================

    def find_all(
        self,
        root=None,
        descendants=True,
    ):
        """
        Return all UI Automation elements under a root.

        Use this carefully: a modern application can expose
        a large UI tree.
        """

        root = root or self.current_element()

        if root is None:
            return []

        condition = (
            self.controller.automation.CreateTrueCondition()
        )

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        collection = root.FindAll(
            scope,
            condition,
        )

        if collection is None:
            return []

        results = []

        try:
            length = collection.Length
        except Exception:
            return results

        for index in range(length):
            try:
                element = collection.GetElement(
                    index
                )

                if element is not None:
                    results.append(
                        element
                    )

            except Exception:
                continue

        return results

    # =========================================================
    # INSPECT ALL
    # =========================================================

    def inspect_all(
        self,
        root=None,
        descendants=True,
        limit=100,
    ):
        """
        Inspect UI elements and return readable dictionaries.

        `limit` prevents accidentally dumping thousands of
        elements from a complex application.
        """

        if limit <= 0:
            return []

        elements = self.find_all(
            root=root,
            descendants=descendants,
        )

        results = []

        for element in elements[:limit]:
            try:
                info = self.inspect(
                    element
                )

                if info:
                    results.append(
                        info
                    )

            except Exception:
                continue

        return results

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        name=None,
        automation_id=None,
        class_name=None,
        control_type=None,
        root=None,
    ):
        """
        Search for a UI element using the strongest available
        semantic property.

        Priority:
            AutomationId
            Name
            ClassName
            ControlType
        """

        if automation_id:
            element = self.find_by_automation_id(
                automation_id,
                root=root,
            )

            if element is not None:
                return element

        if name:
            element = self.find_by_name(
                name,
                root=root,
            )

            if element is not None:
                return element

        if class_name:
            element = self.find_by_class(
                class_name,
                root=root,
            )

            if element is not None:
                return element

        if control_type is not None:
            element = self.find_by_control_type(
                control_type,
                root=root,
            )

            if element is not None:
                return element

        return None

    # =========================================================
    # SEARCH INFO
    # =========================================================

    def search_info(
        self,
        name=None,
        automation_id=None,
        class_name=None,
        control_type=None,
        root=None,
    ):
        """Search and immediately return readable metadata."""

        element = self.search(
            name=name,
            automation_id=automation_id,
            class_name=class_name,
            control_type=control_type,
            root=root,
        )

        if element is None:
            return None

        return self.inspect(
            element
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):
        """Release the underlying UI Automation controller."""

        if self.controller is not None:
            self.controller.close()