class AIExecutor:

    def __init__(
        self,
        llm,
        conversation_manager,
        memory,
    ):
        self.llm = llm
        self.conversation_manager = conversation_manager
        self.memory = memory

    def execute(
        self,
        context,
    ):
        return self.llm.generate(
            prompt=context.command.original,
            history=self.conversation_manager.history(),
            name=self.memory.get_name(),
        )