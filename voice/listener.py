import time

import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from config.states import AssistantState
from core import app_state
from core.logger import logger


class Listener:
    """Capture microphone input and update JARVIS voice state."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5

        self._calibrated = False

        self.last_text = ""
        self.last_time = 0

    def listen(self):
        """Listen for one command and return recognized text."""

        try:
            with self.microphone as source:

                # -------------------------------------------------
                # CALIBRATION
                # -------------------------------------------------

                if not self._calibrated:
                    logger.info(
                        "🎤 Calibrating microphone..."
                    )

                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=1,
                    )

                    self._calibrated = True

                    logger.info(
                        "✅ Calibration complete."
                    )

                # -------------------------------------------------
                # LISTENING STATE
                # -------------------------------------------------

                app_state.state_machine.change(
                    AssistantState.LISTENING
                )

                logger.info(
                    "🎤 Listening..."
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_LIMIT,
                )

            # -----------------------------------------------------
            # RECOGNIZING STATE
            # -----------------------------------------------------

            app_state.state_machine.change(
                AssistantState.THINKING
            )

            logger.info(
                "🧠 Recognizing..."
            )

            text = self.recognizer.recognize_google(
                audio
            )

            audio = None

            text = text.strip().lower()

            # -----------------------------------------------------
            # EMPTY RESULT
            # -----------------------------------------------------

            if not text:
                app_state.state_machine.change(
                    AssistantState.AWAKE
                )

                return ""

            # -----------------------------------------------------
            # DUPLICATE PROTECTION
            # -----------------------------------------------------

            now = time.time()

            if (
                text == self.last_text
                and (now - self.last_time) < 2.5
            ):
                logger.info(
                    "🔁 Duplicate command ignored: %s",
                    text,
                )

                app_state.state_machine.change(
                    AssistantState.AWAKE
                )

                return ""

            self.last_text = text
            self.last_time = now

            logger.info(
                "Recognized: %s",
                text,
            )

            app_state.state_machine.change(
                AssistantState.THINKING
            )

            return text

        # =========================================================
        # VOICE TIMEOUT
        # =========================================================

        except sr.WaitTimeoutError:
            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            return ""

        # =========================================================
        # UNKNOWN SPEECH
        # =========================================================

        except sr.UnknownValueError:
            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            return ""

        # =========================================================
        # RECOGNITION SERVICE ERROR
        # =========================================================

        except sr.RequestError as error:
            logger.error(
                "Speech recognition service error: %s",
                error,
            )

            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            return ""

        # =========================================================
        # MICROPHONE ERROR
        # =========================================================

        except OSError as error:
            logger.exception(
                "Microphone error: %s",
                error,
            )

            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            return ""

        # =========================================================
        # UNKNOWN ERROR
        # =========================================================

        except Exception as error:
            logger.exception(
                "Listener error: %s",
                error,
            )

            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            return ""