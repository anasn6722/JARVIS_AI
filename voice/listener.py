import time

import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from core.logger import logger


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5

        self._calibrated = False

        # Duplicate protection
        self.last_text = ""
        self.last_time = 0

    def listen(self):

        try:

            with self.microphone as source:

                # Calibrate only once
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

            audio = None

            text = text.strip().lower()

            # Ignore empty recognition
            if not text:
                return ""

            # Ignore duplicate commands within 2.5 seconds
            now = time.time()

            if (
                text == self.last_text
                and (now - self.last_time) < 2.5
            ):
                logger.info("🔁 Duplicate command ignored: %s", text)
                return ""

            self.last_text = text
            self.last_time = now

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

        except Exception as error:

            logger.exception(
                "Listener error: %s",
                error,
            )

            return ""