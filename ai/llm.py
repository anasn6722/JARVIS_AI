from google import genai
from google.genai.errors import APIError, ClientError

from config.settings import GEMINI_API_KEY
from core.logger import logger


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

        # Server errors (503), temporary outages, etc.
        except APIError as e:
            logger.error("Gemini API Error: %s", e)
            return "The AI service is temporarily unavailable."

        # Authentication, quota, invalid request, etc.
        except ClientError as e:
            logger.error("Gemini Client Error: %s", e)
            return "I couldn't contact the AI service right now."