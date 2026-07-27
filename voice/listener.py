import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from core.logger import logger


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

                logger.info("🗣️ Speak now...")

                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_LIMIT,
                )

            text = self.recognizer.recognize_google(audio)

            logger.info("Recognized: %s", text)

            return text

        except sr.WaitTimeoutError:
            logger.warning("No speech detected.")
            return ""

        except sr.UnknownValueError:
            logger.warning("Could not understand speech.")
            return ""

        except sr.RequestError as error:
            logger.error("Speech recognition service error: %s", error)
            return ""

        except OSError as error:
            logger.exception("Microphone error: %s", error)
            return ""