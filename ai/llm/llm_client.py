from ai.llm.providers.gemini import GeminiProvider


class LLMClient:

    def __init__(self):

        self.provider = GeminiProvider()

    def generate(
        self,
        model,
        conversation,
    ):

        return self.provider.generate(
            model=model,
            conversation=conversation,
        )