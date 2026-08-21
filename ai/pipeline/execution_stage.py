class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        if not context.commands:
            return

        # Always start a fresh aggregation for this pipeline.

        # =====================================================
        # BUILTIN COMMANDS
        # =====================================================

        for index, item in enumerate(context.commands):

            command = item.get("command")

            if command is None:
                continue

            decision = self._find_decision(
                context,
                command,
            )

            if decision is None:
                continue

            route = getattr(
                decision,
                "route",
                None,
            )

            if route != "BUILTIN":
                continue

            response = self.brain.execute_builtin(
                command.intent,
                command,
            )

            if response:

                command_index = item.get(
                    "command_index",
                    index,
                )

                context.set_command_result(
                    command_index,
                    response,
                )

                print(
                    "COMMAND RESULT:",
                    command_index,
                    "->",
                    response,
                )

        # =====================================================
        # PLANNER / GRAPH EXECUTION
        # =====================================================
        
        if context.tasks:
        
            # Execute the graph.
            self.brain.execution_manager.execute(
                context
            )

            self._assign_planner_results(
                context
            )


        # =====================================================
        # FINAL DEBUG
        # =====================================================

        print(
            "=" * 50
        )

        print(
            "COMMAND RESULTS"
        )

        for key in sorted(
            context.command_results
        ):

            print(
                key,
                "->",
                context.command_results[key],
            )

        print(
            "=" * 50
        )

    # =========================================================
    # GRAPH RESULTS
    # =========================================================

    @staticmethod
    def _assign_planner_results(
        context,
    ):

        for task in context.tasks:

            command_index = getattr(
                task,
                "command_index",
                None,
            )

            if command_index is None:
                continue

            if not task.success:
                continue

            if task.result is None:
                continue

            result = str(
                task.result
            ).strip()

            if not result:
                continue

            # Convert low-level task output into the same
            # human-facing response used by GraphRunner.
            response = ExecutionStage._format_task_result(
                task
            )

            if response:

                context.set_command_result(
                    command_index,
                    response,
                )

    # =========================================================
    # FORMAT TASK RESULT
    # =========================================================

    @staticmethod
    def _format_task_result(task):

        action = str(
            task.action
            or ""
        ).strip()

        target = str(
            task.target
            or ""
        ).strip()

        result = (
            str(task.result)
            .strip()
        )

        # -----------------------------------------------------
        # OPEN
        # -----------------------------------------------------

        if action == "open":

            return f"Opened {target}."

        # -----------------------------------------------------
        # CLOSE
        # -----------------------------------------------------

        if action == "close":

            return f"Closed {target}."

        # -----------------------------------------------------
        # SEARCH UI
        # -----------------------------------------------------

        if action == "search_ui":

            if result:
                return result

            return f"Searched for '{target}'."

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        if action == "search":

            if result:
                return result

            return f"Searched for '{target}'."

        # -----------------------------------------------------
        # YOUTUBE
        # -----------------------------------------------------

        if action == "youtube_search":

            if result:
                return result

            return f"Searched YouTube for '{target}'."

        # -----------------------------------------------------
        # KEYBOARD
        # -----------------------------------------------------

        if action == "keyboard_press":

            return f"Pressed {target}."

        if action == "keyboard_hotkey":

            return f"Pressed {target}."

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        if action == "ui_click_descriptor":

            return f"Clicked {target}."

        if action in {
            "ui_type_descriptor",
            "ui_type",
            "ui_type_at",
        }:

            return (
                result
                or "Text entered successfully."
            )

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return (
            result
            or "Task completed successfully."
        )

    # =========================================================
    # AI COMMAND INDEX
    # =========================================================

    @staticmethod
    def _find_ai_command_index(
        context,
    ):

        for index, item in enumerate(
            context.commands
        ):

            command = item.get(
                "command"
            )

            if command is None:
                continue

            decision = (
                ExecutionStage._find_decision(
                    context,
                    command,
                )
            )

            if decision is None:
                continue

            if getattr(
                decision,
                "route",
                None,
            ) == "AI":

                return item.get(
                    "command_index",
                    index,
                )

        return None

    # =========================================================
    # DECISION LOOKUP
    # =========================================================

    @staticmethod
    def _find_decision(
        context,
        command,
    ):

        for item in context.decisions:

            item_command = item.get(
                "command"
            )

            if item_command is command:

                return item.get(
                    "decision"
                )

            if (
                item_command is not None
                and getattr(
                    item_command,
                    "original",
                    None,
                )
                == getattr(
                    command,
                    "original",
                    None
                )
            ):

                return item.get(
                    "decision"
                )

        return None