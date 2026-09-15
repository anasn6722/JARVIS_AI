from ai.pipeline.context import PipelineContext


class RecoveryStage:
    """
    Recovery after verified failure.

    IMPORTANT:
    Registered local commands NEVER use Gemini for recovery.

    Local/Desktop automation remains completely offline.
    AI recovery is allowed only for genuine AI commands.
    """

    LOCAL_INTENTS = {
        "voice_language",
        "open",
        "close",
        "close_last",
        "list_windows",
        "active_window",
        "find_window",
        "focus_window",
        "close_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "search_ui",
        "open_search_result",
        "path_exists",
        "list_directory",
        "file_info",
        "create_folder",
        "create_file",
        "read_file",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",
        "search",
        "youtube_search",
        "time",
        "identity",
    }

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context: PipelineContext):

        # -----------------------------------------------------
        # Nothing to recover.
        # -----------------------------------------------------

        if context.verified:
            return

        if not context.verification_errors:
            return

        # -----------------------------------------------------
        # Never allow an uncontrolled recovery loop.
        # -----------------------------------------------------

        if context.recovery_attempted:
            return

        context.recovery_attempted = True

        # -----------------------------------------------------
        # Find failed task.
        # -----------------------------------------------------

        failed_tasks = [
            task
            for task in context.tasks
            if not task.success
        ]

        if not failed_tasks:
            return

        failed_task = failed_tasks[0]

        print("=" * 50)
        print("RECOVERY STAGE")
        print("=" * 50)

        print(
            "Failed action:",
            failed_task.action,
        )

        print(
            "Failed target:",
            failed_task.target,
        )

        print(
            "Failure:",
            failed_task.error,
        )

        # =====================================================
        # OFFLINE FIREWALL
        # =====================================================

        if self._is_local_action(
            failed_task.action
        ):

            print("=" * 50)
            print(
                "OFFLINE RECOVERY FIREWALL"
            )
            print("=" * 50)

            print(
                f"Local action '{failed_task.action}' "
                "failed."
            )

            print(
                "Gemini recovery is BLOCKED."
            )

            print(
                "Desktop/local automation remains "
                "100% OFFLINE."
            )

            print("=" * 50)

            context.recovery_task = None

            context.verified = False

            return

        # =====================================================
        # AI RECOVERY
        # =====================================================

        recovery_task = (
            self.brain.recovery_manager.recover(
                failed_task
            )
        )

        if recovery_task is None:

            print(
                "No safe recovery available."
            )

            return

        context.recovery_task = recovery_task

        print(
            "Recovery action:",
            recovery_task.action,
        )

        print(
            "Recovery target:",
            recovery_task.target,
        )

        # ----------------------------------------------------
        # Defensive check:
        # recovery_manager itself must not return a local
        # action through the AI recovery path.
        # ----------------------------------------------------

        if self._is_local_action(
            recovery_task.action
        ):

            print("=" * 50)
            print(
                "RECOVERY LOCAL-ACTION FIREWALL"
            )
            print("=" * 50)

            print(
                f"AI recovery attempted to create "
                f"local action '{recovery_task.action}'."
            )

            print(
                "Blocked."
            )

            print("=" * 50)

            context.recovery_task = None

            return

        # ----------------------------------------------------
        # Build recovery graph.
        # ----------------------------------------------------

        recovery_graph = (
            self.brain.graph_builder.build(
                [recovery_task]
            )
        )

        response = (
            self.brain.execution_engine.execute(
                tasks=[recovery_task],
                graph=recovery_graph,
            )
        )

        # ----------------------------------------------------
        # Verify recovery result.
        # ----------------------------------------------------

        if recovery_task.success:

            context.tasks.append(
                recovery_task
            )

            context.graph = recovery_graph

            context.response = response

            context.verification_errors = []

            context.verified = True

            print(
                "RECOVERY SUCCESSFUL"
            )

            return

        # ----------------------------------------------------
        # Recovery failed.
        # ----------------------------------------------------

        context.verification_errors = [
            recovery_task.error
            or str(response)
            or "Recovery action failed."
        ]

        context.verified = False

        print(
            "RECOVERY FAILED"
        )

    # =========================================================
    # LOCAL ACTION CHECK
    # =========================================================

    @classmethod
    def _is_local_action(
        cls,
        action,
    ):
        if not isinstance(action, str):
            return False

        return (
            action.strip().lower()
            in cls.LOCAL_INTENTS
        )