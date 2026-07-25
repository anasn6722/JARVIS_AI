from PySide6.QtCore import QThread

from voice.speaker import Speaker


class SpeechThread(QThread):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def run(self):
        speaker = Speaker()
        speaker.speak(self.text)