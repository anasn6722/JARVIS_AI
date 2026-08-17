class AgentContext:
    """Shared context passed between JARVIS agents."""

    def __init__(
        self,
        command,
        *,
        brain=None,
        pipeline_context=None,
    ):
        self.command = command
        self.brain = brain
        self.pipeline_context = pipeline_context

        self.agent_name = None
        self.intent = None
        self.entities = {}

        self.result = None
        self.error = None

        self.metadata = {}

    def set_result(self, result):
        self.result = result
        return result

    def set_error(self, error):
        self.error = str(error)
        return self.error