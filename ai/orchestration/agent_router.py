from ai.agents.supervisor import SupervisorAgent
from ai.orchestration.agent_context import AgentContext


class AgentRouter:
    """Entry point for single and multi-agent routing."""

    def __init__(self):

        self.supervisor = (
            SupervisorAgent()
        )

    # =========================================================
    # SINGLE COMMAND
    # =========================================================

    def route(
        self,
        command,
        *,
        brain=None,
        pipeline_context=None,
    ):

        context = AgentContext(
            command,
            brain=brain,
            pipeline_context=pipeline_context,
        )

        return self.supervisor.route(
            command,
            context,
        )

    # =========================================================
    # MULTI COMMAND
    # =========================================================

    def route_many(
        self,
        commands,
        *,
        brain=None,
        pipeline_context=None,
        max_workers=4,
    ):
        """
        Route independent commands to specialist agents.

        Commands must be supplied in their original order.
        """

        if not commands:
            return []

        contexts = []

        for index, command in enumerate(
            commands
        ):

            context = AgentContext(
                command,
                brain=brain,
                pipeline_context=pipeline_context,
            )

            context.metadata[
                "command_index"
            ] = index

            contexts.append(
                (
                    command,
                    context,
                )
            )

        return self.supervisor.route_many(
            contexts,
            max_workers=max_workers,
        )