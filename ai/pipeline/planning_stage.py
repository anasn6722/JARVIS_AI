class PlanningStage:

    def __init__(self, brain):
        self.brain = brain

    # =========================================================
    # RUN
    # =========================================================

    def run(self, context):

        context.tasks = []

        # Keep track of tasks produced by each command.
        command_task_groups = []

        # =========================================================
        # PLAN EACH COMMAND
        # =========================================================

        for command_index, item in enumerate(
            context.decisions
        ):

            command = item["command"]
            decision = item["decision"]

            # -----------------------------------------------------
            # Skip commands that don't require planning.
            # -----------------------------------------------------

            if decision.route != "PLANNER":
                command_task_groups.append([])
                continue

            tasks = self.brain.planning_manager.plan(
                command
            )

            tasks = tasks or []

            for task in tasks:
                task.command_index = command_index

            command_task_groups.append(
                tasks
            )

            context.tasks.extend(
                tasks
            )

        # =========================================================
        # CROSS-COMMAND DEPENDENCIES
        # =========================================================

        self._assign_cross_command_dependencies(
            context,
            command_task_groups,
        )

        # =========================================================
        # BUILD GRAPH
        # =========================================================

        context.graph = self.brain.graph_builder.build(
            context.tasks
        )

        # =========================================================
        # DEBUG
        # =========================================================

        print(
            "=" * 50
        )

        print(
            "ALL PLANNED TASKS"
        )

        for task in context.tasks:

            print(
                task
            )

        print(
            "=" * 50
        )

    # =========================================================
    # CROSS COMMAND DEPENDENCIES
    # =========================================================

    def _assign_cross_command_dependencies(
        self,
        context,
        command_task_groups,
    ):
        """
        Add dependencies between separate user commands.

        Examples:

            open chrome
            search python classes

        becomes:

            open chrome
                ↓
            search python classes

        And:

            search python classes
            open the first result

        becomes:

            search python classes
                ↓
            open_search_result(first)

        Independent commands such as:

            tell me a joke
            what time is it

        remain independent.
        """

        if not command_task_groups:
            return

        # ---------------------------------------------------------
        # Most recent application / website open task.
        # ---------------------------------------------------------

        latest_open_task = None

        # ---------------------------------------------------------
        # Most recent search task.
        # ---------------------------------------------------------

        latest_search_task = None

        # ---------------------------------------------------------
        # Process commands in original order.
        # ---------------------------------------------------------

        for command_index, tasks in enumerate(
            command_task_groups
        ):

            if not tasks:
                continue

            command = None

            if (
                command_index
                < len(context.decisions)
            ):

                command = context.decisions[
                    command_index
                ]["command"]

            command_intent = getattr(
                command,
                "intent",
                "",
            )

            # =====================================================
            # SEARCH UI
            # =====================================================

            if command_intent == "search_ui":

                # Search UI normally requires a visible browser or
                # desktop search surface.
                if latest_open_task is not None:

                    first_search_task = None

                    for task in tasks:

                        if task.action == "search_ui":

                            first_search_task = task
                            break

                    if (
                        first_search_task is not None
                        and latest_open_task.id
                        not in first_search_task.depends_on
                    ):

                        first_search_task.depends_on.append(
                            latest_open_task.id
                        )

                        print(
                            "DEPENDENCY:",
                            first_search_task.id,
                            "->",
                            latest_open_task.id,
                        )

                # ---------------------------------------------
                # Remember the latest search for later
                # search-result references.
                # ---------------------------------------------

                for task in tasks:

                    if task.action == "search_ui":

                        latest_search_task = task
                        break

            # =====================================================
            # SEARCH RESULT REFERENCE
            # =====================================================

            elif command_intent == "search_result":

                result_task = None

                for task in tasks:

                    if task.action == "open_search_result":

                        result_task = task
                        break

                # ---------------------------------------------
                # A search-result reference must follow the
                # most recent search task.
                # ---------------------------------------------

                if (
                    result_task is not None
                    and latest_search_task is not None
                    and latest_search_task.id
                    not in result_task.depends_on
                ):

                    result_task.depends_on.append(
                        latest_search_task.id
                    )

                    print(
                        "SEARCH RESULT DEPENDENCY:",
                        result_task.id,
                        "->",
                        latest_search_task.id,
                    )

            # =====================================================
            # RECORD OPEN TASKS
            # =====================================================

            for task in tasks:

                if task.action == "open":

                    latest_open_task = task

            # =====================================================
            # EXPLICIT SAME-DESKTOP DEPENDENCIES
            # =====================================================

            if command is not None:

                text = str(
                    getattr(
                        command,
                        "original",
                        "",
                    )
                    or ""
                ).lower()

                dependency_phrases = (
                    "last result",
                    "last ui",
                    "previous result",
                    "previous window",
                    "that window",
                    "that button",
                    "it",
                    "then",
                )

                if any(
                    phrase in text
                    for phrase in dependency_phrases
                ):

                    previous_task = (
                        self._find_previous_task(
                            context.tasks,
                            tasks,
                        )
                    )

                    if previous_task is not None:

                        for task in tasks:

                            if (
                                task.id
                                == previous_task.id
                            ):
                                continue

                            if (
                                previous_task.id
                                not in task.depends_on
                            ):

                                task.depends_on.append(
                                    previous_task.id
                                )

    # =========================================================
    # PREVIOUS TASK
    # =========================================================

    @staticmethod
    def _find_previous_task(
        all_tasks,
        current_tasks,
    ):
        """
        Return the nearest task occurring before the current
        command's tasks.
        """

        if not current_tasks:
            return None

        current_ids = {
            task.id
            for task in current_tasks
        }

        previous = None

        for task in all_tasks:

            if task.id in current_ids:
                break

            previous = task

        return previous