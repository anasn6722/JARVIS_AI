
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
            #
            # First convert the user's text into a Command object.
            #
            # Example:
            #
            # "close it"
            #
            # becomes:
            #
            # Command(
            #     original="close it",
            #     intent="close",
            #     entities=...
            # )
            #
            # ====================================================

            command_data, goal = (
                self.brain.command_manager.process(
                    text
                )
            )

            # ====================================================
            # REFERENCE RESOLUTION
            # ====================================================
            #
            # Resolve references AFTER command processing.
            #
            # Example:
            #
            # Previous command:
            #     open youtube
            #
            # Current command:
            #     close it
            #
            # Memory:
            #     ('website', 'youtube')
            #
            # ReferenceResolver changes:
            #
            #     apps: []
            #     websites: ['youtube']
            #
            # ====================================================

            command_data = (
                self.brain.reference_resolver.resolve(
                    command_data
                )
            )

            # ====================================================
            # STORE COMMAND
            # ====================================================

            context.commands.append(
                {
                    "command": command_data,
                    "goal": goal,
                }
            )

        # ========================================================
        # DEBUG
        # ========================================================

        print("=" * 50)
        print("COMMAND STAGE")

        for item in context.commands:

            print(
                item["command"]
            )

        print("=" * 50)
