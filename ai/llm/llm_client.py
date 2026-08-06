from google import genai

from config.settings import GEMINI_API_KEY


class LLMClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        model,
        conversation,
    ):

        response = (
            self.client.models.generate_content(
                model=model,
                contents=conversation,
            )
        )

        return response.text