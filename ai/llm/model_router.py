from google.genai.errors import APIError, ClientError

from ai.model_manager import ModelManager
from core.logger import logger


class ModelRouter:

    def __init__(
        self,
        provider,
    ):
        self.provider = provider
        self.model_manager = ModelManager()

    def generate(
        self,
        conversation,
    ):

        for _ in range(len(self.model_manager.models)):

            model = self.model_manager.current

            try:

                logger.info(
                    "Using AI model: %s",
                    model,
                )

                response = self.provider.generate(
                    model=model,
                    conversation=conversation,
                )

                self.model_manager.reset()

                return response

            except APIError as e:

                logger.warning(
                    "Model %s failed: %s",
                    model,
                    e,
                )

                self.model_manager.next_model()

            except ClientError as e:

                logger.error(
                    "Client Error: %s",
                    e,
                )

                return (
                    "I couldn't connect to the AI service."
                )

        logger.error(
            "All AI models failed."
        )

        self.model_manager.reset()

        return (
            "I'm unable to contact my AI brain right now."
        )