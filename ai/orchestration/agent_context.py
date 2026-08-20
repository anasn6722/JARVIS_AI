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

        self.pipeline_context = (
            pipeline_context
        )

        self.agent_name = None

        self.intent = (
            getattr(
                command,
                "intent",
                None,
            )
        )

        self.entities = (
            getattr(
                command,
                "entities",
                {},
            )
            or {}
        )

        self.result = None

        self.error = None

        self.metadata = {}

    # =========================================================
    # RESULT
    # =========================================================

    def set_result(
        self,
        result,
    ):

        self.result = result

        return result

    # =========================================================
    # ERROR
    # =========================================================

    def set_error(
        self,
        error,
    ):

        self.error = str(
            error
        )

        return self.error

    # =========================================================
    # SUCCESS
    # =========================================================

    @property
    def success(self):

        if self.error:
            return False

        if self.result is None:
            return False

        return bool(
            getattr(
                self.result,
                "success",
                True,
            )
        )