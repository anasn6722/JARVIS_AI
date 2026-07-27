import time

from PySide6.QtCore import QThread, Signal

from config.states import AssistantState
from core import app_state
from core.logger import logger
from voice.listener import Listener
from voice.wake_word import WakeWordDetector


class WakeWordThread(QThread):
    wake_detected = Signal(str)

    def __init__(self):
        super().__init__()

        self.listener = Listener()
        self.detector = WakeWordDetector()
        self._running = True

    def run(self):
        logger.info("Wake word thread started.")

        while self._running:

            if app_state.assistant_state == AssistantState.SLEEPING:
                text = self.listener.listen()

                if not text:
                    continue

                detected, command = self.detector.detect(text)

                if detected:
                    app_state.assistant_state = AssistantState.AWAKE

                    app_state.last_active = time.time()

                    self.wake_detected.emit(command)

            else:
                self.msleep(200)

    def stop(self):
        self._running = False