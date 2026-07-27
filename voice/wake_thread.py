import threading
import time

from core.logger import logger
from voice.wake_word import WakeWordDetector


class WakeWordThread(threading.Thread):

    def __init__(self):
        super().__init__()

        self.detector = WakeWordDetector()
        self._running = True


    def run(self):

        logger.info("Wake word listener started.")

        while self._running:

            # Temporary simulation
            # Microphone integration comes next

            text = input("Say something: ")

            detected, command = self.detector.detect(text)

            if detected:
                logger.info("Wake word detected.")
                logger.info("Command: %s", command)
            time.sleep(0.1)


    def stop(self):

        self._running = False

        