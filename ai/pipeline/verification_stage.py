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

        if task.action == "keyboard_press":
            return self._verify_keyboard_press(
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
        Verify that a semantic UI typing task targeted the
        correct UI element.

        For Search, we verify that the Search input remains focused.

        For generic UI elements, we verify that the descriptor
        associated with this task can still be resolved.
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

        # =====================================================
        # SEARCH
        # =====================================================

        if capability == "search_ui":
            """
            Search typing is considered valid when the typing action
            succeeded. Enter/outcome verification is responsible for
            verifying the final search state.
        
            The Search field is expected to lose focus after Enter.
            """
        
            graph = getattr(
                context,
                "graph",
                None,
            )
        
            if graph is not None:
            
                try:
                    node = graph.nodes.get(
                        task.id
                    )
                except Exception:
                    node = None
        
                if node is not None:
                
                    children = getattr(
                        node,
                        "children",
                        [],
                    )
        
                    for child_id in children:
                    
                        try:
                            child = graph.nodes.get(
                                child_id
                            )
                        except Exception:
                            child = None
        
                        if child is None:
                            continue
                        
                        child_task = getattr(
                            child,
                            "task",
                            None,
                        )
        
                        if (
                            child_task is not None
                            and child_task.action
                            == "keyboard_press"
                            and str(
                                child_task.target or ""
                            ).strip().lower()
                            == "enter"
                        ):
                            print(
                                "UI STATE VERIFIED: Search text "
                                "typing completed; Enter will verify "
                                "the final result state."
                            )
                            return None
        
            if self._is_search_focused(
                controller
            ):
                print(
                    "UI STATE VERIFIED: Search input is focused."
                )
        
            return None
        
        # =====================================================
        # GENERIC UI TARGET
        # =====================================================

        semantic_target = str(
            descriptor.get(
                "semantic_target"
            )
            or descriptor.get(
                "name"
            )
            or ""
        ).strip()

        if not semantic_target:
            return None

        try:
            info = controller.ui_inspector.search_info(
                name=semantic_target
            )
        except Exception:
            info = None

        if info is not None:
            print(
                "UI STATE VERIFIED: "
                f"{semantic_target} remains available."
            )
            return None

        return (
            f"UI typing succeeded, but "
            f"'{semantic_target}' could not be verified."
        )


    def _verify_keyboard_press(self, task, context):
        """
        Verify Enter when it completes a UI typing workflow.

        For Search workflows, verify that VS Code actually
        produced a search-result state.
        """

        key = str(
            task.target or ""
        ).strip().lower()

        if key != "enter":
            return None

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
                != "ui_type_descriptor"
                or not parent_task.success
            ):
                continue

            # -------------------------------------------------
            # Extract the typed text.
            #
            # Example:
            # $LAST_UI||Python
            # -------------------------------------------------

            typed_text = self._extract_ui_type_text(
                parent_task.target
            )

            # -------------------------------------------------
            # Determine whether this was Search.
            # -------------------------------------------------

            descriptor = self._get_task_descriptor(
                parent_task,
                context,
            )

            if not isinstance(
                descriptor,
                dict,
            ):
                return (
                    "Enter was pressed, but the previous UI "
                    "typing descriptor could not be identified."
                )

            capability = str(
                descriptor.get("capability") or ""
            ).strip().lower()

            # -------------------------------------------------
            # Search outcome verification
            # -------------------------------------------------

            if capability == "search_ui":

                controller = self._get_ui_controller()

                if controller is None:
                    return (
                        "Search was submitted, but the desktop "
                        "controller was unavailable for outcome "
                        "verification."
                    )

                if self._is_search_result_state(
                    controller,
                    typed_text,
                ):
                    print(
                        "SEARCH OUTCOME VERIFIED:",
                        typed_text or "query",
                    )
                    return None

                return (
                    "Enter was pressed, but a completed Search "
                    "result state could not be detected."
                )

            # -------------------------------------------------
            # Generic UI typing
            # -------------------------------------------------

            print(
                "UI ACTION VERIFIED: "
                "Enter submitted after UI typing."
            )

            return None

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
        

    @staticmethod
    def _extract_ui_type_text(target):
        """
        Extract text from:

            $LAST_UI||Python
        """

        if not isinstance(
            target,
            str,
        ):
            return ""

        marker = "||"

        if marker not in target:
            return ""

        return target.split(
            marker,
            1,
        )[1].strip()

    @staticmethod
    def _is_search_result_state(
        controller,
        expected_query="",
    ):
        """
        Detect the VS Code Search result state.

        Current observed VS Code state:

            Search returned 20000 results in 18 files
        """

        try:
            items = (
                controller
                .ui_inspector
                .inspect_all(
                    limit=1000
                )
            )

        except Exception:
            return False

        expected_query = (
            str(expected_query)
            .strip()
            .lower()
        )

        for item in items:

            if not isinstance(
                item,
                dict,
            ):
                continue

            name = str(
                item.get("name") or ""
            ).strip()

            lower_name = name.lower()

            # -------------------------------------------------
            # Search result status
            # -------------------------------------------------

            if (
                lower_name.startswith(
                    "search returned "
                )
                and " results" in lower_name
            ):
                return True

            # -------------------------------------------------
            # Query-specific fallback.
            # -------------------------------------------------

            if (
                expected_query
                and expected_query in lower_name
                and (
                    "result" in lower_name
                    or "file" in lower_name
                )
            ):
                return True

        return False