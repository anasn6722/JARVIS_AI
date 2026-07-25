from PySide6.QtCore import QThread, Signal

from voice.listener import Listener


class ListenerThread(QThread):
    recognized = Signal(str)

    def __init__(self):
        super().__init__()

        self.listener = Listener()

    def run(self):
        text = self.listener.listen()

        print(f"📡 Thread recognized: {text}")

        self.recognized.emit(text)