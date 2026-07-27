from PySide6.QtCore import QThread, Signal

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
            text = self.listener.listen()

            if not text:
                continue

            detected, command = self.detector.detect(text)

            if detected:
                logger.info("Wake word detected.")
                self.wake_detected.emit(command)

    def stop(self):
        self._running = False