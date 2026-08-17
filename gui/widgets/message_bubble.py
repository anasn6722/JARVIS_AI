from datetime import datetime, timezone

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class MessageBubble(QFrame):
    """HUD-style conversation message."""

    def __init__(
        self,
        sender: str,
        message: str,
        is_user: bool = False,
    ):
        super().__init__()

        self.setObjectName(
            "userBubble"
            if is_user
            else "jarvisBubble"
        )

        self.setMaximumWidth(
            560
        )

        self.setMinimumWidth(
            120
        )

        if is_user:
            bubble_color = "rgba(13, 66, 77, 235)"
            border_color = "#2b9baa"
            sender_color = "#a8f6ff"
        else:
            bubble_color = "rgba(5, 20, 27, 245)"
            border_color = "#155360"
            sender_color = "#7cecff"

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {bubble_color};
                border: 1px solid {border_color};
                border-radius: 13px;
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            11,
            14,
            9,
        )

        layout.setSpacing(
            5
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = QLabel(
            sender.upper()
        )

        header.setStyleSheet(
            f"""
            color: {sender_color};
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
            """
        )

        # =====================================================
        # MESSAGE
        # =====================================================

        message_label = QLabel(
            str(message)
        )

        message_label.setWordWrap(
            True
        )

        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        message_label.setStyleSheet(
            """
            color: #d9faff;
            font-size: 13px;
            line-height: 1.4;
            """
        )

        # =====================================================
        # TIME
        # =====================================================

        timestamp = (
            datetime.now(
                timezone.utc
            )
            .astimezone()
            .strftime("%I:%M %p")
        )

        time_label = QLabel(
            timestamp
        )

        time_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        time_label.setStyleSheet(
            """
            color: #4f7c84;
            font-size: 8px;
            """
        )

        layout.addWidget(
            header
        )

        layout.addWidget(
            message_label
        )

        layout.addWidget(
            time_label
        )