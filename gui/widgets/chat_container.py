from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from gui.widgets.message_bubble import MessageBubble


class ChatContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def add_message(
        self,
        sender: str,
        message: str,
        is_user: bool = False,
    ):
        bubble = MessageBubble(
            sender,
            message,
            is_user,
        )

        self.layout.insertWidget(
            self.layout.count() - 1,
            bubble,
        )