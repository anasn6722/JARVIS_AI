from PySide6.QtCore import QThread

from voice.speaker import Speaker


class SpeechThread(QThread):

    def __init__(
        self,
        text,
        language=None,
    ):
        super().__init__()

        self.text = text
        self.language = language

        self.speaker = Speaker()

    def run(self):
        self.speaker.speak(
            self.text,
            self.language,
        )