import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from core.logger import logger


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        # Better recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self._calibrated = False

    def listen(self):

        try:

            with sr.Microphone() as source:

                # Calibrate ONLY once
                if not self._calibrated:

                    logger.info("🎤 Calibrating microphone...")

                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=1,
                    )

                    self._calibrated = True

                    logger.info("✅ Calibration complete.")

                logger.info("🎤 Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_LIMIT,
                )

            logger.info("🧠 Recognizing...")

            text = self.recognizer.recognize_google(audio)

            text = text.strip().lower()

            logger.info("Recognized: %s", text)

            return text

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""

        except sr.RequestError as error:

            logger.error(
                "Speech recognition service error: %s",
                error,
            )

            return ""

        except OSError as error:

            logger.exception(
                "Microphone error: %s",
                error,
            )

            return ""