import time

from PySide6.QtCore import QThread, Signal

from config.states import AssistantState
from core import app_state
from core.logger import logger
from voice.listener import Listener
from voice.wake_word import WakeWordDetector


class VoiceManager(QThread):
    wake_detected = Signal(str)
    command_detected = Signal(str)

    def __init__(self):
        super().__init__()

        self.listener = Listener()
        self.detector = WakeWordDetector()
        self.running = True

        # Prevent repeated commands
        self.last_command = ""
        self.last_command_time = 0

    def stop(self):
        self.running = False

    def run(self):
        logger.info("Voice Manager started.")

        while self.running:

            # -------------------------------------------------
            # Never listen while Jarvis is speaking/thinking
            # -------------------------------------------------
            while (
                app_state.state_machine.is_speaking()
                or app_state.state_machine.is_thinking()
            ):
                self.msleep(600)
                continue

            # -------------------------------------------------
            # Small delay after speaking
            # Prevents hearing its own voice
            # -------------------------------------------------
            if app_state.state_machine.is_awake():
                self.msleep(900)

            text = self.listener.listen()

            if not text:
                continue

            text = text.strip().lower()

            if len(text) < 2:
                continue

            # -------------------------------------------------
            # Ignore duplicate commands
            # -------------------------------------------------
            now = time.time()

            if (
                text == self.last_command
                and (now - self.last_command_time) < 3
            ):
                logger.info(
                    "Duplicate command ignored: %s",
                    text,
                )
                continue

            self.last_command = text
            self.last_command_time = now

            # -------------------------------------------------
            # Sleeping state
            # -------------------------------------------------
            if app_state.state_machine.is_sleeping():

                detected, command = self.detector.detect(text)

                if detected:

                    app_state.state_machine.change(
                        AssistantState.AWAKE
                    )

                    app_state.last_active = time.time()

                    self.wake_detected.emit(command)

            # -------------------------------------------------
            # Awake state
            # -------------------------------------------------
            elif app_state.state_machine.is_awake():

                app_state.last_active = time.time()

                self.command_detected.emit(text)