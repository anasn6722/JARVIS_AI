from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ai.brain import Brain


class ChatPage(QWidget):
    def __init__(self):
        super().__init__()

        # Brain
        self.brain = Brain()

        # Main Layout
        layout = QVBoxLayout()

        # Title
        title = QLabel("💬 JARVIS Chat")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:white;
        """)

        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        # Input Box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")

        # Send Button
        self.send_button = QPushButton("Send")

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input_box)
        bottom_layout.addWidget(self.send_button)

        # Assemble Layout
        layout.addWidget(title)
        layout.addWidget(self.chat_area)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Events
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)
        self.show_welcome_message()

    def send_message(self):
        command = self.input_box.text().strip()

        if not command:
            return

        self.chat_area.append(f"<b>You:</b> {command}")

        response = self.brain.process(command)

        self.chat_area.append(f"<b>JARVIS:</b> {response}")

        self.chat_area.append("")

        self.input_box.clear()

    def show_welcome_message(self):
        self.chat_area.append(
        "<b style='color:#00D9FF;'>🤖 JARVIS:</b> "
        "Hello Anas! 👋<br>"
        "Welcome back.<br>"
        "How can I help you today?<br>"
    )    