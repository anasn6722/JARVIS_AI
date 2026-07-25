from PySide6.QtCore import QThread, Signal

from voice.listener import Listener


class ListenerThread(QThread):
    finished = Signal(str)

    def __init__(self):
        super().__init__()
        self.listener = Listener()

    def run(self):
        text = self.listener.listen()
        self.finished.emit(text)