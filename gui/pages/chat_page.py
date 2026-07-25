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
from voice.speech_thread import SpeechThread
from voice.listener_thread import ListenerThread


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
        self.voice_button = QPushButton("🎤")

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input_box)
        bottom_layout.addWidget(self.voice_button)
        bottom_layout.addWidget(self.send_button)

        # Assemble Layout
        layout.addWidget(title)
        layout.addWidget(self.scroll)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Events
        self.send_button.clicked.connect(self.send_message)
        self.voice_button.clicked.connect(self.listen_voice)
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
        self.scroll_to_bottom()

        self.chat_container.add_message(
        "🤖 JARVIS",
        "Typing...",
        False,
        )
        self.scroll_to_bottom()
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
        self.scroll_to_bottom()
        self.speech_thread = SpeechThread(response)
        self.speech_thread.start()    

    def show_welcome_message(self):
        self.chat_container.add_message(
        "🤖 JARVIS",
        "Hello Anas! 👋\nWelcome back.\nHow can I help you today?",
        False,
        )
        self.scroll_to_bottom()

    def listen_voice(self):
        self.chat_container.add_message(
        "🤖 JARVIS",
        "🎤 Listening...",
        False,
        )
        self.scroll_to_bottom()

        self.voice_thread = ListenerThread()
        self.voice_thread.finished.connect(self.voice_finished)
        self.voice_thread.start()


    def voice_finished(self, text):
        if not text:
            self.chat_container.add_message(
            "🤖 JARVIS",
            "Sorry, I couldn't hear you.",
            False,
            )
            self.scroll_to_bottom()
            return

        self.input_box.setText(text)
        self.send_message()

    def scroll_to_bottom(self):
        scrollbar = self.scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum()) 