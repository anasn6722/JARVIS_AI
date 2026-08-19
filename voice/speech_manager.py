import time
from queue import Queue

from config.states import AssistantState
from core import app_state
from voice.language_manager import language_manager
from voice.speech_thread import SpeechThread


class SpeechManager:

    def __init__(self):
        self.queue = Queue()
        self.thread = None

    def say(
        self,
        text: str,
        language=None,
    ):
        print(
            "🔊 SpeechManager received:",
            text,
        )

        app_state.state_machine.change(
            AssistantState.SPEAKING
        )

        # -----------------------------------------------------
        # Select response language.
        # -----------------------------------------------------

        if language is None:

            language = (
                language_manager
                .get_response_language()
            )

        self.queue.put(
            (
                text,
                language,
            )
        )

        if (
            self.thread is None
            or not self.thread.isRunning()
        ):
            self._start_next()

    def _start_next(self):

        if self.queue.empty():
            return

        text, language = (
            self.queue.get()
        )

        self.thread = SpeechThread(
            text,
            language,
        )

        self.thread.finished.connect(
            self._speech_finished
        )

        self.thread.start()

    def _speech_finished(self):

        if self.queue.empty():

            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            app_state.last_active = (
                time.time()
            )

        self._start_next()