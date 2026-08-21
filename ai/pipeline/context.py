class PipelineContext:

    def __init__(self, text):

        self.input = text

        # =====================================================
        # COMMANDS
        # =====================================================

        self.commands = []

        # Ordered responses for each user command.
        self.command_results = {}

        # =====================================================
        # DECISIONS
        # =====================================================

        self.decisions = []

        self.current_command = None
        self.current_goal = None
        self.decision = None

        # =====================================================
        # WORKFLOW
        # =====================================================

        self.tasks = []
        self.graph = None

        # =====================================================
        # RESPONSE
        # =====================================================

        self.response = None

        # =====================================================
        # VERIFICATION
        # =====================================================

        self.verified = False
        self.verification_errors = []

        # =====================================================
        # RECOVERY
        # =====================================================

        self.recovery_attempted = False
        self.recovery_task = None

        # =====================================================
        # PIPELINE CONTROL
        # =====================================================

        self.stop = False

    # =========================================================
    # COMMAND RESULT
    # =========================================================

    def set_command_result(
        self,
        command_index,
        response,
    ):
        if response is None:
            return

        response = str(response).strip()

        if not response:
            return

        self.command_results[
            int(command_index)
        ] = response

    # =========================================================
    # ORDERED RESULTS
    # =========================================================

    def ordered_command_results(self):

        return [
            self.command_results[index]
            for index in sorted(
                self.command_results
            )
        ]