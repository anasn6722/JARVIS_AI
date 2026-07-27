from queue import Queue

from voice.speech_thread import SpeechThread


class SpeechManager:
    def __init__(self):
        self.queue = Queue()
        self.thread = None

    def say(self, text: str):
        self.queue.put(text)

        if self.thread is None or not self.thread.isRunning():
            self._start_next()

    def _start_next(self):
        if self.queue.empty():
            return

        text = self.queue.get()

        self.thread = SpeechThread(text)
        self.thread.finished.connect(self._start_next)
        self.thread.start()