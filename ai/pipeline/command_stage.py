class CommandStage:

    def __init__(self, brain):
        self.brain = brain

    # ============================================================
    # RUN COMMAND STAGE
    # ============================================================

    def run(self, context):

        commands = self.brain.command_splitter.split(
            context.input
        )

        context.commands = []

        if not commands:
            return

        # ========================================================
        # SINGLE COMMAND
        # ========================================================

        if len(commands) == 1:

            text = commands[0]

            item = self._process_single_command(
                text,
                context,
                command_index=0,
            )

            context.commands.append(
                item
            )

        # ========================================================
        # MULTIPLE COMMANDS
        # ========================================================

        else:

            self._process_multiple_commands(
                commands,
                context,
            )

        # ========================================================
        # DEBUG
        # ========================================================

        self._print_commands(
            context
        )

    # ============================================================
    # SINGLE COMMAND
    # ============================================================

    def _process_single_command(
        self,
        text,
        context,
        command_index,
    ):

        command_data, goal = (
            self.brain.command_manager.process(
                text
            )
        )

        # --------------------------------------------------------
        # REFERENCE RESOLUTION
        # --------------------------------------------------------

        command_data = (
            self.brain.reference_resolver.resolve(
                command_data
            )
        )

        # --------------------------------------------------------
        # AGENT ROUTING
        # --------------------------------------------------------

        agent_result = (
            self.brain.agent_router.route(
                command_data,
                brain=self.brain,
                pipeline_context=context,
            )
        )

        item = {
            "command": command_data,
            "goal": goal,
            "original_text": text,
            "command_index": command_index,
            "agent": "unassigned",
            "agent_result": None,
        }

        if agent_result is not None:

            item["agent_result"] = (
                agent_result
            )

            item["agent"] = getattr(
                agent_result,
                "agent",
                "unassigned",
            )

        # --------------------------------------------------------
        # INDEX
        # --------------------------------------------------------

        if agent_result is not None:
            metadata = getattr(
                agent_result,
                "metadata",
                None,
            )

            if isinstance(
                metadata,
                dict,
            ):
                metadata[
                    "command_index"
                ] = command_index

        return item

    # ============================================================
    # MULTIPLE COMMANDS
    # ============================================================

    def _process_multiple_commands(
        self,
        commands,
        context,
    ):

        # --------------------------------------------------------
        # First parse every command.
        #
        # We must parse before deciding whether parallel execution
        # is safe.
        # --------------------------------------------------------

        parsed = []

        for index, text in enumerate(
            commands
        ):

            command_data, goal = (
                self.brain.command_manager.process(
                    text
                )
            )

            command_data = (
                self.brain.reference_resolver.resolve(
                    command_data
                )
            )

            parsed.append(
                {
                    "command": command_data,
                    "goal": goal,
                    "original_text": text,
                    "index": index,
                }
            )

        # --------------------------------------------------------
        # Decide whether commands are independent.
        # --------------------------------------------------------

        if self._can_parallelize(
            parsed
        ):

            print(
                "MULTI-AGENT MODE: "
                "parallel execution enabled."
            )

            commands_only = [
                item["command"]
                for item in parsed
            ]

            results = (
                self.brain.agent_router.route_many(
                    commands_only,
                    brain=self.brain,
                    pipeline_context=context,
                )
            )

            # ----------------------------------------------------
            # Rebuild context.commands in original order.
            # ----------------------------------------------------

            result_by_index = {}

            for result in results:

                result_context = (
                    result.get(
                        "context"
                    )
                )

                metadata = getattr(
                    result_context,
                    "metadata",
                    {},
                )

                index = metadata.get(
                    "command_index",
                    0,
                )

                result_by_index[
                    index
                ] = result

            for item in parsed:

                index = item["index"]

                result = (
                    result_by_index.get(
                        index
                    )
                )

                agent_result = (
                    result.get(
                        "result"
                    )
                    if result
                    else None
                )

                agent_name = (
                    getattr(
                        agent_result,
                        "agent",
                        "unassigned",
                    )
                    if agent_result
                    else "unassigned"
                )

                context.commands.append(
                    {
                        "command": item[
                            "command"
                        ],
                        "goal": item[
                            "goal"
                        ],
                        "original_text": item[
                            "original_text"
                        ],
                        "agent": agent_name,
                        "agent_result": agent_result,
                    }
                )

        else:

            # ----------------------------------------------------
            # Sequential fallback.
            #
            # Required for:
            #   close it
            #   click it
            #   type it
            #   use last result
            #   dependent operations
            # ----------------------------------------------------

            print(
                "MULTI-AGENT MODE: "
                "sequential dependency mode."
            )

            for item in parsed:

                command_data = item[
                    "command"
                ]

                agent_result = (
                    self.brain.agent_router.route(
                        command_data,
                        brain=self.brain,
                        pipeline_context=context,
                    )
                )

                agent_name = (
                    getattr(
                        agent_result,
                        "agent",
                        "unassigned",
                    )
                    if agent_result
                    else "unassigned"
                )

                context.commands.append(
                    {
                        "command": command_data,
                        "goal": item[
                            "goal"
                        ],
                        "original_text": item[
                            "original_text"
                        ],
                        "agent": agent_name,
                        "agent_result": agent_result,
                    }
                )

    # ============================================================
    # PARALLELIZATION RULES
    # ============================================================

    @staticmethod
    def _can_parallelize(
        parsed_commands,
    ):
        """
        Determine whether multiple commands are independent.

        Parallel execution is disabled when references or
        dependency language is present.
        """

        if len(
            parsed_commands
        ) <= 1:
            return False

        dependency_phrases = (
            "it",
            "that",
            "this",
            "those",
            "the result",
            "last result",
            "last ui",
            "previous",
            "after that",
            "then",
            "next",
            "same",
            "again",
        )

        for item in parsed_commands:

            text = (
                item["original_text"]
                .lower()
                .strip()
            )

            # ----------------------------------------------------
            # Reference/dependency wording
            # ----------------------------------------------------

            if any(
                phrase in text
                for phrase in dependency_phrases
            ):
                return False

            # ----------------------------------------------------
            # Explicit task dependencies
            # ----------------------------------------------------

            command = item[
                "command"
            ]

            goal = getattr(
                command,
                "goal",
                None,
            )

            if isinstance(
                goal,
                dict,
            ):

                if goal.get(
                    "parent_goal"
                ):
                    return False

        return True

    # ============================================================
    # DEBUG
    # ============================================================

    @staticmethod
    def _print_commands(
        context
    ):

        print(
            "=" * 50
        )

        print(
            "COMMAND STAGE"
        )

        for index, item in enumerate(
            context.commands
        ):

            print(
                f"Command {index + 1}:",
                item["command"],
            )

            print(
                "Agent:",
                item.get(
                    "agent",
                    "unassigned",
                ),
            )

        print(
            "=" * 50
        )