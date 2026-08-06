class CommandStage:

    def __init__(self, brain):
        self.brain = brain


    def run(self, context):

        commands = self.brain.command_splitter.split(
            context.input
        )


        context.commands = []


        for text in commands:

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


            context.commands.append(
                {
                    "command": command_data,
                    "goal": goal,
                }
            )


        print("=" * 50)
        print("COMMAND STAGE")

        for item in context.commands:
            print(
                item["command"]
            )

        print("=" * 50)