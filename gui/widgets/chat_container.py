from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.message_bubble import MessageBubble


class ChatContainer(QWidget):
    """Scrollable JARVIS conversation container."""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            12,
            14,
            12,
            14,
        )

        self.layout.setSpacing(
            10
        )

        self.layout.addStretch()

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

        row = QHBoxLayout()

        row.setContentsMargins(
            4,
            0,
            4,
            0,
        )

        if is_user:
            row.addStretch()
            row.addWidget(
                bubble,
                0,
            )
        else:
            row.addWidget(
                bubble,
                0,
            )
            row.addStretch()

        self.layout.insertLayout(
            self.layout.count() - 1,
            row,
        )