from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class CommandConsole(QFrame):
    """Holographic-style command transmission console."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "commandConsole"
        )

        self.setStyleSheet(
            """
            QFrame#commandConsole {
                background-color: rgba(3, 14, 19, 235);
                border: 1px solid #15505c;
                border-radius: 12px;
            }

            QLabel#consoleHeader {
                color: #70e8f5;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#consoleIndicator {
                color: #55f0cc;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#consoleText {
                color: #d6fbff;
                font-size: 12px;
                font-family: Consolas;
            }

            QLabel#consoleMeta {
                color: #4d8d98;
                font-size: 9px;
                font-family: Consolas;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(4)

        # =====================================================
        # HEADER
        # =====================================================

        header_row = QHBoxLayout()

        header = QLabel(
            "JARVIS // COMMAND TRANSMISSION"
        )

        header.setObjectName(
            "consoleHeader"
        )

        indicator = QLabel(
            "● ONLINE"
        )

        indicator.setObjectName(
            "consoleIndicator"
        )

        header_row.addWidget(
            header
        )

        header_row.addStretch()

        header_row.addWidget(
            indicator
        )

        layout.addLayout(
            header_row
        )

        # =====================================================
        # COMMAND
        # =====================================================

        self.command_label = QLabel(
            "> waiting for command..."
        )

        self.command_label.setObjectName(
            "consoleText"
        )

        self.command_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.command_label
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        self.response_label = QLabel(
            "JARVIS: system ready."
        )

        self.response_label.setObjectName(
            "consoleText"
        )

        self.response_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.response_label
        )

        # =====================================================
        # META
        # =====================================================

        self.meta_label = QLabel(
            "CHANNEL: LOCAL // STATUS: READY"
        )

        self.meta_label.setObjectName(
            "consoleMeta"
        )

        layout.addWidget(
            self.meta_label
        )

    # =========================================================
    # COMMAND
    # =========================================================

    def show_command(self, command):
        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.command_label.setText(
            f"> {command}"
        )

        self.meta_label.setText(
            f"{timestamp} // CHANNEL: LOCAL // "
            "STATUS: PROCESSING"
        )

    # =========================================================
    # RESPONSE
    # =========================================================

    def show_response(self, response):
        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.response_label.setText(
            f"JARVIS: {response}"
        )

        self.meta_label.setText(
            f"{timestamp} // CHANNEL: LOCAL // "
            "STATUS: COMPLETE"
        )

    # =========================================================
    # PROCESSING
    # =========================================================

    def show_processing(self):
        self.response_label.setText(
            "JARVIS: processing command..."
        )

        self.meta_label.setText(
            "CHANNEL: LOCAL // STATUS: THINKING"
        )

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(self, message):
        self.response_label.setText(
            f"JARVIS: {message}"
        )

        self.meta_label.setText(
            "CHANNEL: LOCAL // STATUS: ERROR"
        )