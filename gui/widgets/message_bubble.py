from datetime import datetime, timezone

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class MessageBubble(QFrame):
    def __init__(
        self,
        sender: str,
        message: str,
        is_user: bool = False,
    ):
        super().__init__()

        self.setMaximumWidth(450)

        if is_user:
            bubble_color = "#2E7D32"
            sender_color = "#A5D6A7"
        else:
            bubble_color = "#2B2B2B"
            sender_color = "#00D9FF"

        self.setStyleSheet(
            f"""
            QFrame {{
                background:{bubble_color};
                border-radius:15px;
                padding:12px;
            }}

            QLabel {{
                color:white;
                background:transparent;
            }}
            """
        )

        layout = QVBoxLayout()

        # Sender
        sender_label = QLabel(sender)
        sender_label.setStyleSheet(
            f"""
            color:{sender_color};
            font-weight:bold;
            font-size:14px;
            """
        )

        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            font-size:15px;
        """)

        # Time
        time_label = QLabel(
        datetime.now(timezone.utc)
        .astimezone()
        .strftime("%I:%M %p")
)

        time_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        time_label.setStyleSheet("""
            color:gray;
            font-size:11px;
        """)

        layout.addWidget(sender_label)
        layout.addWidget(message_label)
        layout.addWidget(time_label)

        self.setLayout(layout)