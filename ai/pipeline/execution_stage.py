class ExecutionStage:

    def __init__(self, brain):
        self.brain = brain

    def run(self, context):

        # AI requests should be handled by AIStage.
        if context.decision and context.decision.route == "AI":
            print("AI route detected. Skipping ExecutionStage.")
            return

        self.brain.execution_manager.execute(context)

        context.stop = True