class MemoryStage:

    def __init__(self, brain):

        self.brain = brain

    def run(self, context):

        memory = self.brain.auto_memory.extract(
            context.input
        )

        if memory:

            key, value = memory

            self.brain.memory.remember(
                key,
                value,
            )