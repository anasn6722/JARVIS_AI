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
from config.constants import CHAT_TYPING_DELAY
from config.states import AssistantState
from core import app_state
from core.app_state import speech_manager
from gui.widgets.chat_container import ChatContainer
from voice.listener_thread import ListenerThread
from voice.wake_word_thread import WakeWordThread


class ChatPage(QWidget):
    def __init__(self):
        super().__init__()

        # Brain
        self.brain = Brain()
        # Assistant State
        self.state = AssistantState.SLEEPING
        # Listening Animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(
        self.animate_listening
        )

        self.animation_step = 0
        
        

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

        # Voice Status
        self.voice_status = QLabel("Ready")
        self.voice_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.voice_status.setStyleSheet("""
            QLabel{
                color:#4CAF50;
                font-size:14px;
                font-weight:bold;
        }
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
        self.voice_button.setFixedWidth(60)

        self.voice_button.setStyleSheet("""
        QPushButton{
        background:#00BCD4;
        color:white;
        font-size:20px;
        border-radius:10px;
        padding:8px;
        }

        QPushButton:hover{
        background:#00ACC1;
        }

        QPushButton:pressed{
        background:#00838F;
        }

        QPushButton:disabled{
        background:#555555;
        }
        """)

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input_box)
        bottom_layout.addWidget(self.voice_button)
        bottom_layout.addWidget(self.send_button)

        # Assemble Layout
        layout.addWidget(title)
        layout.addWidget(self.voice_status)
        layout.addWidget(self.scroll)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Events
        self.send_button.clicked.connect(self.send_message)
        self.voice_button.clicked.connect(self.listen_voice)
        self.input_box.returnPressed.connect(self.send_message)
        self.show_welcome_message()
        self.wake_thread = WakeWordThread()

        self.wake_thread.wake_detected.connect(
            self.on_wake_detected
        )

        self.wake_thread.start()

        

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

        if command != "__WAKE__":
            self.chat_container.add_message(
                "🤖 JARVIS",
                "Typing...",
                False,
            )
        self.scroll_to_bottom()
        self.input_box.clear()

        QTimer.singleShot(
            CHAT_TYPING_DELAY,
            self.generate_response,
        )

    def generate_response(self):

        if self.current_command == "__WAKE__":
            speech_manager.say("Yes?")

            self.chat_container.add_message(
                "🤖 JARVIS",
                "Yes?",
                False,
            )

            self.scroll_to_bottom()
            return

        response = self.brain.process(
            self.current_command
        )

        if not response:
            response = "Sorry, I couldn't process that request."

        self.chat_container.add_message(
            "🤖 JARVIS",
            response,
            False,
        )

        self.scroll_to_bottom()

        speech_manager.say(response)
        self.state = AssistantState.SPEAKING 

    def show_welcome_message(self):
        self.chat_container.add_message(
        "🤖 JARVIS",
        "Hello Anas! 👋\nWelcome back.\nHow can I help you today?",
        False,
        )
        self.scroll_to_bottom()

    def listen_voice(self):
        self.voice_button.setEnabled(False)

      # Start Listening Animation
        self.animation_step = 0
        self.animation_timer.start(400)

        self.voice_thread = ListenerThread()
        self.voice_thread.recognized.connect(self.voice_finished)
        self.voice_thread.start()


    def voice_finished(self, text):
        
        self.animation_timer.stop()
        self.voice_button.setEnabled(True)
        self.voice_status.setText("Ready")

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
        self.state = AssistantState.SLEEPING

    def on_wake_detected(self, command):
        self.chat_container.add_message(
            "🤖 JARVIS",
            "Yes?",
            False,
        )

        self.scroll_to_bottom()

        speech_manager.say("Yes?")

        if command:
            self.input_box.setText(command)
            self.send_message()    

    def scroll_to_bottom(self):
        scrollbar = self.scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum()) 

    def animate_listening(self):
        dots = "." * ((self.animation_step % 3) + 1)

        self.voice_status.setText(
        f"🎙️ Listening{dots}"
        )

        self.animation_step += 1    

    def closeEvent(self, event):
        if hasattr(self, "wake_thread"):
            self.wake_thread.stop()
            self.wake_thread.wait()

        event.accept()    