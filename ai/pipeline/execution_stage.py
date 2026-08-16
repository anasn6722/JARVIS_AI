class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        if context.decision is None:
            return

        # =========================================================
        # AI ROUTE
        # =========================================================

        if context.decision.route == "AI":
            return

        # =========================================================
        # BUILTIN ROUTE
        # =========================================================

        if context.decision.route == "BUILTIN":

            command = None

            # CommandStage stores parsed commands here.
            if context.commands:

                last_item = context.commands[-1]

                if isinstance(
                    last_item,
                    dict,
                ):
                    command = last_item.get(
                        "command"
                    )

            if command is None:
                context.response = None
                return None

            response = self.brain.execute_builtin(
                context.decision.intent,
                command.original,
            )

            context.response = response

            return response

        # =========================================================
        # NORMAL PLANNER / DESKTOP EXECUTION
        # =========================================================

        return self.brain.execution_manager.execute(
            context
        )