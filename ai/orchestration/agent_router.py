from ai.agents.supervisor import SupervisorAgent
from ai.orchestration.agent_context import AgentContext


class AgentRouter:
    """Entry point for multi-agent command routing."""

    def __init__(self):
        self.supervisor = SupervisorAgent()

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