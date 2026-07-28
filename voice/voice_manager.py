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

    def stop(self):
        self.running = False

    def run(self):
        logger.info("Voice Manager started.")

        while self.running:

            # Don't listen while speaking or thinking
            while (
                app_state.state_machine.is_speaking()
                or app_state.state_machine.is_thinking()
            ):            
                self.msleep(200)
                continue

            if app_state.state_machine.is_awake():
                self.msleep(300)             

            text = self.listener.listen()

            if not text:
                continue

            # Ignore commands shorter than 2 characters
            if len(text.strip()) < 2:
                continue

            if app_state.state_machine.is_sleeping():

                detected, command = self.detector.detect(text)

                if detected:
                    app_state.state_machine.change(
                        AssistantState.AWAKE
                    )
                    app_state.last_active = time.time()
                    self.wake_detected.emit(command)

            elif app_state.state_machine.is_awake():

                app_state.last_active = time.time()
                self.command_detected.emit(text)