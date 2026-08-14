from desktop_automation.controller.ui_automation_controller import (
    UIAutomationController,
)


class UIElementInspector:
    """
    High-level semantic UI element search.

    Uses Windows UI Automation through UIAutomationController.
    """

    TREE_SCOPE_ELEMENT = 0x1
    TREE_SCOPE_CHILDREN = 0x2
    TREE_SCOPE_DESCENDANTS = 0x4

    UIA_NAME_PROPERTY_ID = 30005
    UIA_AUTOMATION_ID_PROPERTY_ID = 30011
    UIA_CLASSNAME_PROPERTY_ID = 30012
    UIA_CONTROLTYPE_PROPERTY_ID = 30003

    def __init__(self, controller=None):
        self.controller = (
            controller
            or UIAutomationController()
        )

    # =========================================================
    # CURRENT WINDOW
    # =========================================================

    def current_window(self):
        return self.controller.foreground_window()

    # =========================================================
    # CURRENT ELEMENT
    # =========================================================

    def current_element(self):
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
        if element is None:
            return None

        return self.controller.inspect_element(
            element
        )

    # =========================================================
    # CREATE CONDITION
    # =========================================================

    def _property_condition(
        self,
        property_id,
        value,
    ):
        """
        Create a UI Automation property condition.

        comtypes handles conversion of the Python value to the
        appropriate VARIANT.
        """

        return self.controller.automation.CreatePropertyCondition(
            property_id,
            value,
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
        """Find an element by name, case-insensitively."""
    
        if not name:
            return None
    
        root = root or self.current_element()
    
        if root is None:
            return None
    
        wanted = str(name).strip().lower()
    
        # ---------------------------------------------------------
        # Search the UI tree directly.
        #
        # We intentionally inspect the actual CurrentName values
        # instead of relying only on CreatePropertyCondition,
        # because voice/text normalization can change casing.
        # ---------------------------------------------------------
    
        elements = self.find_all(
            root=root,
            descendants=descendants,
        )
    
        for element in elements:
            try:
                current_name = (
                    element.CurrentName or ""
                ).strip()
    
                if not current_name:
                    continue
                
                if current_name.lower() != wanted:
                    continue
                
                # -------------------------------------------------
                # Make sure the element has usable bounds.
                # -------------------------------------------------
    
                try:
                    rect = element.CurrentBoundingRectangle
    
                    width = (
                        int(rect.right)
                        - int(rect.left)
                    )
    
                    height = (
                        int(rect.bottom)
                        - int(rect.top)
                    )
    
                    if width <= 0 or height <= 0:
                        continue
                    
                except Exception:
                    continue
                
                return element
    
            except Exception:
                continue
            
        return None

    # =========================================================
    # FIND BY AUTOMATION ID
    # =========================================================

    def find_by_automation_id(
        self,
        automation_id,
        root=None,
        descendants=True,
    ):
        if not automation_id:
            return None

        root = root or self.current_element()

        if root is None:
            return None

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        try:
            condition = self._property_condition(
                self.UIA_AUTOMATION_ID_PROPERTY_ID,
                str(automation_id),
            )

            return root.FindFirst(
                scope,
                condition,
            )

        except Exception:
            pass

        wanted = (
            str(automation_id)
            .strip()
            .lower()
        )

        for element in self.find_all(
            root=root,
            descendants=descendants,
        ):
            try:
                current_id = (
                    element.CurrentAutomationId
                    or ""
                )

                if (
                    current_id.strip().lower()
                    == wanted
                ):
                    return element

            except Exception:
                continue

        return None

    # =========================================================
    # FIND BY CLASS NAME
    # =========================================================

    def find_by_class(
        self,
        class_name,
        root=None,
        descendants=True,
    ):
        if not class_name:
            return None

        root = root or self.current_element()

        if root is None:
            return None

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        try:
            condition = self._property_condition(
                self.UIA_CLASSNAME_PROPERTY_ID,
                str(class_name),
            )

            element = root.FindFirst(
                scope,
                condition,
            )

            if element is not None:
                return element

        except Exception:
            pass

        wanted = (
            str(class_name)
            .strip()
            .lower()
        )

        for element in self.find_all(
            root=root,
            descendants=descendants,
        ):
            try:
                current_class = (
                    element.CurrentClassName
                    or ""
                )

                if (
                    current_class.strip().lower()
                    == wanted
                ):
                    return element

            except Exception:
                continue

        return None

    # =========================================================
    # FIND BY CONTROL TYPE
    # =========================================================

    def find_by_control_type(
        self,
        control_type,
        root=None,
        descendants=True,
    ):
        root = root or self.current_element()

        if root is None:
            return None

        try:
            control_type = int(
                control_type
            )
        except (TypeError, ValueError):
            return None

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        try:
            condition = self._property_condition(
                self.UIA_CONTROLTYPE_PROPERTY_ID,
                control_type,
            )

            element = root.FindFirst(
                scope,
                condition,
            )

            if element is not None:
                return element

        except Exception:
            pass

        for element in self.find_all(
            root=root,
            descendants=descendants,
        ):
            try:
                if (
                    int(element.CurrentControlType)
                    == control_type
                ):
                    return element

            except Exception:
                continue

        return None

    # =========================================================
    # FIND AT POINT
    # =========================================================

    def find_at_point(self, x, y):
        return self.controller.element_from_point(
            int(x),
            int(y),
        )

    # =========================================================
    # INSPECT AT POINT
    # =========================================================

    def inspect_at_point(self, x, y):
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
    # FIND ALL
    # =========================================================

    def find_all(
        self,
        root=None,
        descendants=True,
    ):
        root = root or self.current_element()

        if root is None:
            return []

        scope = (
            self.TREE_SCOPE_DESCENDANTS
            if descendants
            else self.TREE_SCOPE_CHILDREN
        )

        try:
            condition = (
                self.controller.automation.CreateTrueCondition()
            )

            collection = root.FindAll(
                scope,
                condition,
            )

        except Exception:
            return []

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
        # Prefer the most stable identifier.

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
        if self.controller is not None:
            self.controller.close()