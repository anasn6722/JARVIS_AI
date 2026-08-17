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

        # ========================================================
        # PROCESS COMMANDS
        # ========================================================

        for text in commands:

            # ====================================================
            # COMMAND MANAGER
            # ====================================================

            command_data, goal = (
                self.brain.command_manager.process(
                    text
                )
            )

            # ====================================================
            # REFERENCE RESOLUTION
            # ====================================================

            command_data = (
                self.brain.reference_resolver.resolve(
                    command_data
                )
            )

            # ====================================================
            # MULTI-AGENT ROUTING
            # ====================================================

            agent_context = {
                "command": command_data,
                "goal": goal,
                "original_text": text,
            }

            agent_result = self.brain.agent_router.route(
                command_data,
                brain=self.brain,
                pipeline_context=context,
            )

            if agent_result is not None:
                agent_context[
                    "agent_result"
                ] = agent_result

                agent_context[
                    "agent"
                ] = getattr(
                    agent_result,
                    "agent",
                    "",
                )

            else:
                agent_context[
                    "agent"
                ] = "unassigned"

            # ====================================================
            # STORE COMMAND
            # ====================================================

            context.commands.append(
                agent_context
            )

        # ========================================================
        # DEBUG
        # ========================================================

        print("=" * 50)
        print("COMMAND STAGE")

        for item in context.commands:

            print(
                "Command:",
                item["command"],
            )

            print(
                "Agent:",
                item.get(
                    "agent",
                    "unassigned",
                ),
            )

        print("=" * 50)