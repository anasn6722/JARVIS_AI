from PySide6.QtCore import QThread

from config.states import AssistantState
from core import app_state
from voice.speaker import Speaker


class SpeechThread(QThread):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):

        speaker = Speaker()
        speaker.speak(self.text)

        