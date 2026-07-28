import time
from queue import Queue

from config.states import AssistantState
from core import app_state
from voice.speech_thread import SpeechThread


class SpeechManager:

    def __init__(self):
        self.queue = Queue()
        self.thread = None

    def say(self, text: str):

        app_state.state_machine.change(
            AssistantState.SPEAKING
        )

        self.queue.put(text)

        if self.thread is None or not self.thread.isRunning():
            self._start_next()

    def _start_next(self):

        if self.queue.empty():

            return

        text = self.queue.get()

        self.thread = SpeechThread(text)
        self.thread.finished.connect(self._speech_finished)
        self.thread.start()

    def _speech_finished(self):

        if self.queue.empty():
            time.sleep(0.8)      # 0.5–1.0 seconds
            app_state.state_machine.change(
                AssistantState.AWAKE
            )

        self._start_next()