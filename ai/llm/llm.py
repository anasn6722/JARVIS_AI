from google import genai
from google.genai.errors import APIError, ClientError

from ai.model_manager import ModelManager
from ai.prompt import build_prompt
from config.settings import GEMINI_API_KEY
from core.logger import logger


class LLM:
    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )

        self.model_manager = ModelManager()

    def ask(
        self,
        prompt,
        history=None,
        name="User",
    ):
        system_prompt = build_prompt(name)

        conversation = [system_prompt]

        if history:
            for item in history:
                conversation.append(
                    f"{item['speaker']}: {item['message']}"
                )

        conversation.append(f"User: {prompt}")

        # Try every model
        for _ in range(len(self.model_manager.models)):
            try:
                logger.info(
                    "Using AI model: %s",
                    self.model_manager.current,
                )

                response = self.client.models.generate_content(
                    model=self.model_manager.current,
                    contents=conversation,
                )

                self.model_manager.reset()
                return response.text

            except APIError as e:
                logger.warning(
                    "Model %s failed: %s",
                    self.model_manager.current,
                    e,
                )
                self.model_manager.next_model()

            except ClientError as e:
                logger.error(
                    "Client Error: %s",
                    e,
                )
                return "I couldn't connect to the AI service."

        logger.error("All AI models failed.")
        self.model_manager.reset()

        return "I'm unable to contact my AI brain right now."

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