from PySide6.QtCore import QThread, Signal

from core.logger import logger
from voice.listener import Listener
from voice.wake_word import WakeWordDetector


class ListenerThread(QThread):
    recognized = Signal(str)

    def __init__(self):
        super().__init__()

        self.listener = Listener()
        self.detector = WakeWordDetector()

    def run(self):
        text = self.listener.listen()

        logger.info("Thread recognized: %s", text)

        if not text:
            return

        detected, command = self.detector.detect(text)

        if detected:
            print("🎤 Wake word detected!")

            if command:
                self.recognized.emit(command)
            else:
                self.recognized.emit("__WAKE__")
        else:
            print("😴 Wake word not detected.")