class VerificationStage:
    """
    Verify completed pipeline tasks.

    Verification has two layers:

        1. Basic task-result verification.
        2. UI-state verification for semantic UI actions.

    UI-state verification is intentionally conservative.
    It only performs extra checks when the task provides enough
    information to verify a meaningful state change.
    """

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # PUBLIC API
    # =========================================================

    def run(self, context):
        """Verify the results of all executable tasks."""

        # Normal AI conversation does not have executable tasks.
        if not context.tasks:
            context.verified = True
            context.verification_errors = []
            return

        errors = []

        for task in context.tasks:

            # -------------------------------------------------
            # Basic task result
            # -------------------------------------------------

            if not task.success:
                errors.append(
                    task.error
                    or f"Task failed: {task.action}"
                )
                continue

            # -------------------------------------------------
            # State-aware verification
            # -------------------------------------------------

            state_error = self._verify_task_state(
                task
            )

            if state_error:
                errors.append(
                    state_error
                )

        context.verification_errors = errors
        context.verified = not errors

        # =====================================================
        # OUTPUT
        # =====================================================

        if errors:
            print("=" * 50)
            print("VERIFICATION FAILED")
            print("=" * 50)

            for error in errors:
                print(error)

        else:
            print("=" * 50)
            print("VERIFICATION PASSED")
            print("=" * 50)

    # =========================================================
    # STATE VERIFICATION
    # =========================================================

    def _verify_task_state(self, task):
        """
        Verify actual UI state after a successful task.

        Returns:
            None when verification succeeds or is not applicable.
            str when verification fails.
        """

        if task.action == "ui_click_descriptor":
            return self._verify_ui_click(
                task
            )

        if task.action == "ui_type_descriptor":
            return self._verify_ui_type(
                task
            )

        return None

    # =========================================================
    # UI CONTROLLER
    # =========================================================

    def _get_ui_controller(self):
        """
        Obtain the DesktopController through the registered
        ui_find_descriptor tool.

        This avoids depending on a hard-coded Brain attribute name.
        """

        try:
            tool = self.brain.tool_registry.get(
                "ui_find_descriptor"
            )

            if tool is None:
                return None

            callback = tool.callback

            controller = getattr(
                callback,
                "__self__",
                None,
            )

            return controller

        except Exception:
            return None

    # =========================================================
    # GRAPH TASK CONTEXT
    # =========================================================

    def _get_last_ui_descriptor(self):
        """
        Return the most recently resolved UI descriptor from the
        current GraphRunner task context.
        """

        try:
            graph_runner = (
                self.brain
                .execution_engine
                .workflow_manager
                .graph_runner
            )

            return graph_runner.task_context.get(
                "last_ui"
            )

        except Exception:
            return None

    # =========================================================
    # CLICK VERIFICATION
    # =========================================================

    def _verify_ui_click(self, task):
        """
        Verify a successful semantic UI click.

        Capability-based elements use their semantic state rather
        than requiring the old UI Automation element to remain alive.
        """

        descriptor = (
            self._get_last_ui_descriptor()
        )

        if not isinstance(
            descriptor,
            dict,
        ):
            return (
                "UI click succeeded, but no UI descriptor "
                "was available for state verification."
            )

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        controller = (
            self._get_ui_controller()
        )

        if controller is None:
            return (
                "UI click succeeded, but the desktop controller "
                "was unavailable for state verification."
            )

        # =====================================================
        # EXPLORER
        # =====================================================

        if capability == "explorer_ui":
            if self._is_explorer_visible(
                controller
            ):
                print(
                    "UI STATE VERIFIED: Explorer is visible."
                )
                return None

            return (
                "Explorer shortcut succeeded, but Explorer "
                "was not detected in the current UI."
            )

        # =====================================================
        # SEARCH
        # =====================================================

        if capability == "search_ui":
            if self._is_search_visible(
                controller
            ):
                print(
                    "UI STATE VERIFIED: Search is visible."
                )
                return None

            return (
                "Search action succeeded, but Search "
                "was not detected in the current UI."
            )

        # =====================================================
        # NORMAL UI ELEMENT
        # =====================================================

        name = str(
            descriptor.get("name") or ""
        ).strip()

        if not name:
            return None

        try:
            info = controller.ui_inspector.search_info(
                name=name
            )

        except Exception:
            info = None

        if info is not None:
            print(
                f"UI STATE VERIFIED: {name} is visible."
            )
            return None

        return (
            f"UI action succeeded, but '{name}' "
            "is no longer detectable."
        )

    # =========================================================
    # TYPE VERIFICATION
    # =========================================================

    def _verify_ui_type(self, task):
        """
        Verify that a semantic UI typing action has a valid
        destination and a successful result.

        For generic text fields, the current keyboard action
        already provides the strongest deterministic signal.

        Capability-based Search receives an additional focused
        UI check when available.
        """

        descriptor = (
            self._get_last_ui_descriptor()
        )

        if not isinstance(
            descriptor,
            dict,
        ):
            return (
                "UI typing succeeded, but no UI descriptor "
                "was available for verification."
            )

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        controller = (
            self._get_ui_controller()
        )

        if controller is None:
            return (
                "UI typing succeeded, but the desktop controller "
                "was unavailable for verification."
            )

        # =====================================================
        # SEARCH
        # =====================================================

        if capability == "search_ui":
            if self._is_search_focused(
                controller
            ):
                print(
                    "UI STATE VERIFIED: Search input is focused."
                )
                return None

            # Search may change state immediately after typing,
            # so do not automatically fail solely because the
            # original action element is no longer visible.
            return None

        return None

    # =========================================================
    # SEARCH STATE
    # =========================================================

    @staticmethod
    def _is_search_visible(controller):
        """Return True when the VS Code Search action is visible."""

        try:
            info = controller.ui_inspector.search_info(
                name="Search (Ctrl+Shift+F)"
            )

            return info is not None

        except Exception:
            return False

    # =========================================================
    # EXPLORER STATE
    # =========================================================

    @staticmethod
    def _is_explorer_visible(controller):
        """
        Return True when Explorer-related UI is visible.

        We first look for the standard Explorer action.
        Then we check common Explorer section labels.
        """

        try:
            inspector = controller.ui_inspector

            # -------------------------------------------------
            # Explorer action
            # -------------------------------------------------

            info = inspector.search_info(
                name="Explorer (Ctrl+Shift+E)"
            )

            if info is not None:
                return True

            # -------------------------------------------------
            # Explorer section
            # -------------------------------------------------

            for name in (
                "EXPLORER",
                "Explorer",
                "Explorer Section: JARVIS_AI",
            ):
                info = inspector.search_info(
                    name=name
                )

                if info is not None:
                    return True

            # -------------------------------------------------
            # Broad inspection fallback
            # -------------------------------------------------

            items = inspector.inspect_all(
                limit=500
            )

            for item in items:
                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                name = str(
                    item.get("name") or ""
                ).strip().lower()

                if name in {
                    "explorer",
                    "explorer section: jarvis_ai",
                }:
                    return True

            return False

        except Exception:
            return False

    # =========================================================
    # FOCUSED SEARCH STATE
    # =========================================================

    @staticmethod
    def _is_search_focused(controller):
        """Return True when the focused control looks like Search."""

        try:
            focused = (
                controller
                .ui_inspector
                .controller
                .focused_element()
            )

            if focused is None:
                return False

            name = str(
                focused.CurrentName or ""
            ).strip().lower()

            class_name = str(
                focused.CurrentClassName or ""
            ).strip().lower()

            search_terms = (
                "search",
                "type search term",
            )

            if any(
                term in name
                for term in search_terms
            ):
                return True

            if "search" in class_name:
                return True

            return False

        except Exception:
            return False