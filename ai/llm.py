from google import genai
from google.genai.errors import ClientError

from config.settings import GEMINI_API_KEY


class LLM:
    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )

    def ask(self, prompt: str):
        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )

            return response.text

        except ClientError as e:
            print(f"Gemini API Error: {e}")
            return None