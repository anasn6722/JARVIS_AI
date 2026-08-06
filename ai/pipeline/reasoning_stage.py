class ReasoningStage:

    def __init__(self, brain):
        self.brain = brain


    def run(self, context):

        context.decisions = []


        for item in context.commands:

            command = item["command"]


            decision = (
                self.brain.reasoning.decide(
                    command
                )
            )


            context.decisions.append(
                {
                    "command": command,
                    "decision": decision,
                }
            )


            print("=" * 50)
            print("REASONING")
            print(decision)
            print("=" * 50)