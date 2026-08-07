from ai.llm.manager import LLMManager


class LLM:

    def __init__(self):
        self.manager = LLMManager()

    def ask(
        self,
        prompt,
        history=None,
        name="User",
    ):
        return self.manager.ask(
            prompt=prompt,
            history=history,
            name=name,
        )

    def chat(
        self,
        prompt,
        history=None,
        name="User",
    ):
        return self.manager.chat(
            prompt=prompt,
            history=history,
            name=name,
        )