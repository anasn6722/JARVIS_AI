import threading
import time

from voice.wake_word import WakeWordDetector


class WakeWordThread(threading.Thread):

    def __init__(self):
        super().__init__()

        self.detector = WakeWordDetector()
        self.running = True


    def run(self):

        print("Wake word listener started...")

        while self.running:

            # Temporary simulation
            # Microphone integration comes next

            text = input("Say something: ")

            if self.detector.detect(text):
                print("🎤 Wake word detected!")

            time.sleep(0.1)


    def stop(self):

        self.running = False

        