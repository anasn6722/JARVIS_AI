import time

from PySide6.QtCore import QThread, Signal

from config.states import AssistantState
from core import app_state
from core.logger import logger
from voice.listener import Listener
from voice.wake_word import WakeWordDetector


class VoiceManager(QThread):
    """Background voice loop for wake-word and commands."""

    wake_detected = Signal(str)
    command_detected = Signal(str)

    def __init__(self):
        super().__init__()

        self.listener = Listener()
        self.detector = WakeWordDetector()

        self.running = True

        self.last_command = ""
        self.last_command_time = 0.0

        self._listening = False

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):
        self.running = False

    # =========================================================
    # STATUS
    # =========================================================

    @property
    def is_listening(self):
        return self._listening

    # =========================================================
    # MAIN LOOP
    # =========================================================

    def run(self):
        logger.info(
            "Voice Manager started."
        )

        while self.running:

            # -------------------------------------------------
            # WAIT WHILE THINKING / SPEAKING
            # -------------------------------------------------

            if (
                app_state.state_machine.is_thinking()
                or app_state.state_machine.is_speaking()
            ):
                self._listening = False

                self.msleep(
                    250
                )

                continue

            # -------------------------------------------------
            # SMALL DELAY AFTER SPEECH
            # -------------------------------------------------

            if app_state.state_machine.is_awake():

                self._listening = False

                self.msleep(
                    700
                )

            if not self.running:
                break

            # -------------------------------------------------
            # REMEMBER STATE BEFORE LISTENING
            # -------------------------------------------------

            was_sleeping = (
                app_state.state_machine.is_sleeping()
            )

            self._listening = True

            logger.info(
                "Voice state before listen: %s",
                (
                    "SLEEPING"
                    if was_sleeping
                    else "AWAKE"
                ),
            )

            # -------------------------------------------------
            # LISTEN
            # -------------------------------------------------

            text = self.listener.listen()

            self._listening = False

            if not self.running:
                break

            if not text:
                # Return to an appropriate idle state.
                if was_sleeping:
                    app_state.state_machine.change(
                        AssistantState.SLEEPING
                    )
                else:
                    app_state.state_machine.change(
                        AssistantState.AWAKE
                    )

                continue

            text = text.strip().lower()

            if len(text) < 2:
                continue

            logger.info(
                "Recognized: %s",
                text,
            )

            # -------------------------------------------------
            # DUPLICATE PROTECTION
            # -------------------------------------------------

            now = time.time()

            if (
                text == self.last_command
                and (
                    now
                    - self.last_command_time
                ) < 3
            ):
                logger.info(
                    "Duplicate command ignored: %s",
                    text,
                )

                if was_sleeping:
                    app_state.state_machine.change(
                        AssistantState.SLEEPING
                    )
                else:
                    app_state.state_machine.change(
                        AssistantState.AWAKE
                    )

                continue

            self.last_command = text
            self.last_command_time = now

            # =================================================
            # SLEEPING → WAKE WORD
            # =================================================

            if was_sleeping:

                detected, command = (
                    self.detector.detect(
                        text
                    )
                )

                if not detected:

                    app_state.state_machine.change(
                        AssistantState.SLEEPING
                    )

                    continue

                app_state.state_machine.change(
                    AssistantState.AWAKE
                )

                app_state.last_active = (
                    time.time()
                )

                logger.info(
                    "Wake word detected. Command: %s",
                    command or "(none)",
                )

                self.wake_detected.emit(
                    command
                )

                continue

            # =================================================
            # AWAKE → NORMAL COMMAND
            # =================================================

            app_state.state_machine.change(
                AssistantState.THINKING
            )

            app_state.last_active = (
                time.time()
            )

            logger.info(
                "Voice command detected: %s",
                text,
            )

            self.command_detected.emit(
                text
            )

            # -------------------------------------------------
            # IMPORTANT
            # -------------------------------------------------
            #
            # Do not exit.
            #
            # ChatPage processes the command.
            # SpeechManager moves through SPEAKING → AWAKE.
            # The loop then starts listening again.
            #
            continue

        self._listening = False

        logger.info(
            "Voice Manager stopped."
        )