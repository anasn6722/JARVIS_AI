from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ai.brain import Brain
from gui.widgets.chat_container import ChatContainer


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

        # Chat Container
        self.chat_container = ChatContainer()

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_container)

        self.scroll.setStyleSheet("""
        QScrollArea{
        border:none;
        background:#1E1E1E;
        }
        """)

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
        layout.addWidget(self.scroll)
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

        self.current_command = command

        self.chat_container.add_message(
        "🧑 You",
        command,
        True,
        )

        self.chat_container.add_message(
        "🤖 JARVIS",
        "Typing...",
        False,
        )

        self.input_box.clear()

        QTimer.singleShot(
        1000,
        self.generate_response,
        )

    def generate_response(self):
        response = self.brain.process(
        self.current_command
        )

        self.chat_container.add_message(
        "🤖 JARVIS",
        response,
        False,
        )    

    def show_welcome_message(self):
        self.chat_container.add_message(
        "🤖 JARVIS",
        "Hello Anas! 👋\nWelcome back.\nHow can I help you today?",
        False,
        )
    