from ai.llm.conversation_builder import ConversationBuilder
from ai.llm.llm_client import LLMClient
from ai.llm.model_router import ModelRouter
from ai.llm.prompt_builder import build_prompt
from ai.llm.providers.gemini import GeminiProvider


class LLMManager:

    def __init__(self):

        self.client = LLMClient()

        self.router = ModelRouter(
            self.client,
        )

        self.conversation_builder = ConversationBuilder()

    def ask(
        self,
        prompt,
        history=None,
        name="User",
    ):

        system_prompt = build_prompt(name)

        conversation = self.conversation_builder.build(
            system_prompt=system_prompt,
            history=history,
            prompt=prompt,
        )

        return self.router.generate(
            conversation,
        )

    def chat(
        self,
        prompt,
        history=None,
        name="User",
    ):

        return self.ask(
            prompt=prompt,
            history=history,
            name=name,
        )