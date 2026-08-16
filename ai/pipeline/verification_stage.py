class VerificationStage:
    """
    Verify completed pipeline tasks.

    Verification has two layers:

        1. Basic task-result verification.
        2. State-aware verification for semantic UI actions.

    UI verification uses the descriptor produced by the task's
    own dependency chain rather than the global LAST_UI value.
    """

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # PUBLIC API
    # =========================================================

    def run(self, context):
        """Verify the results of all executable tasks."""

        if not context.tasks:
            context.verified = True
            context.verification_errors = []
            return

        errors = []

        for task in context.tasks:

            if not task.success:
                errors.append(
                    task.error
                    or f"Task failed: {task.action}"
                )
                continue

            state_error = self._verify_task_state(
                task,
                context,
            )

            if state_error:
                errors.append(state_error)

        context.verification_errors = errors
        context.verified = not errors

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
    # TASK STATE VERIFICATION
    # =========================================================

    def _verify_task_state(self, task, context):
        """Verify state for actions that have a meaningful UI state."""

        if task.action == "ui_click_descriptor":
            return self._verify_ui_click(
                task,
                context,
            )

        if task.action == "ui_type_descriptor":
            return self._verify_ui_type(
                task,
                context,
            )

        return None

    # =========================================================
    # UI CONTROLLER
    # =========================================================

    def _get_ui_controller(self):
        """Get the DesktopController behind the registered UI tool."""

        try:
            tool = self.brain.tool_registry.get(
                "ui_find_descriptor"
            )

            if tool is None:
                return None

            callback = tool.callback

            return getattr(
                callback,
                "__self__",
                None,
            )

        except Exception:
            return None

    # =========================================================
    # TASK DESCRIPTOR
    # =========================================================

    def _get_task_descriptor(self, task, context):
        """
        Get the descriptor belonging to this task.

        For ui_click_descriptor / ui_type_descriptor tasks,
        the descriptor should come from the immediately preceding
        ui_find_descriptor dependency, not the global LAST_UI.
        """

        graph = getattr(
            context,
            "graph",
            None,
        )

        if graph is None:
            return None

        try:
            node = graph.nodes.get(
                task.id
            )
        except Exception:
            node = None

        if node is None:
            return None

        # -----------------------------------------------------
        # Check direct parents first.
        # -----------------------------------------------------

        parent_ids = getattr(
            node,
            "parents",
            [],
        )

        for parent_id in parent_ids:

            try:
                parent = graph.nodes.get(
                    parent_id
                )
            except Exception:
                parent = None

            if parent is None:
                continue

            parent_task = getattr(
                parent,
                "task",
                None,
            )

            if parent_task is None:
                continue

            if (
                parent_task.action
                == "ui_find_descriptor"
                and parent_task.success
            ):
                result = parent_task.result

                if isinstance(
                    result,
                    dict,
                ):
                    return result

        # -----------------------------------------------------
        # Fallback: search all completed find-descriptor tasks.
        # -----------------------------------------------------

        try:
            nodes = graph.nodes.values()
        except Exception:
            nodes = []

        for candidate in nodes:

            candidate_task = getattr(
                candidate,
                "task",
                None,
            )

            if candidate_task is None:
                continue

            if (
                candidate_task.action
                == "ui_find_descriptor"
                and candidate_task.success
                and isinstance(
                    candidate_task.result,
                    dict,
                )
            ):
                return candidate_task.result

        return None

    # =========================================================
    # CLICK VERIFICATION
    # =========================================================

    def _verify_ui_click(self, task, context):
        """
        Verify the UI state produced by this specific click task.
        """

        descriptor = self._get_task_descriptor(
            task,
            context,
        )

        if not isinstance(
            descriptor,
            dict,
        ):
            return (
                "UI click succeeded, but its source UI descriptor "
                "could not be identified."
            )

        controller = self._get_ui_controller()

        if controller is None:
            return (
                "UI click succeeded, but the desktop controller "
                "was unavailable for state verification."
            )

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        semantic_target = str(
            descriptor.get("semantic_target") or ""
        ).strip()

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
                "Explorer action succeeded, but Explorer "
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
        # NORMAL UI TARGET
        # =====================================================

        name = (
            semantic_target
            or str(
                descriptor.get("name") or ""
            ).strip()
        )

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

    def _verify_ui_type(self, task, context):
        """
        Verify a UI typing task using its own source descriptor.
        """

        descriptor = self._get_task_descriptor(
            task,
            context,
        )

        if not isinstance(
            descriptor,
            dict,
        ):
            return (
                "UI typing succeeded, but its source UI descriptor "
                "could not be identified."
            )

        controller = self._get_ui_controller()

        if controller is None:
            return (
                "UI typing succeeded, but the desktop controller "
                "was unavailable for verification."
            )

        capability = str(
            descriptor.get("capability") or ""
        ).strip().lower()

        if capability == "search_ui":
            if self._is_search_focused(
                controller
            ):
                print(
                    "UI STATE VERIFIED: Search input is focused."
                )

            # Search can change UI state immediately after typing.
            return None

        # Generic UI typing already has a successful keyboard
        # result; the descriptor identifies the destination.
        return None

    # =========================================================
    # SEARCH STATE
    # =========================================================

    @staticmethod
    def _is_search_visible(controller):
        """Return True when the Search action is visible."""

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
        """Return True when Explorer-related UI is visible."""

        try:
            inspector = controller.ui_inspector

            # -------------------------------------------------
            # Standard Explorer action
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
            # Broad fallback
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
    # SEARCH FOCUS
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

            if (
                "search" in name
                or "type search term" in name
            ):
                return True

            if "search" in class_name:
                return True

            return False

        except Exception:
            return False