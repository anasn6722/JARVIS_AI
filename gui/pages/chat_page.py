import time

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
from config.constants import (
    AWAKE_TIMEOUT,
    CHAT_TYPING_DELAY,
)
from config.states import AssistantState
from core import app_state
from core.app_state import speech_manager
from gui.widgets.chat_container import ChatContainer
from voice.voice_manager import VoiceManager


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        # Brain
        self.brain = Brain()
        

        # Assistant State
        app_state.state_machine.change(
            AssistantState.SLEEPING
        )

        # Listening Animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(
            self.animate_listening
        )

        self.animation_step = 0


        # Sleep Timer
        self.sleep_timer = QTimer()
        self.sleep_timer.timeout.connect(
            self.check_sleep_timeout
        )
        self.sleep_timer.start(1000)


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
        self.voice_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

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
        self.scroll.setWidget(
            self.chat_container
        )

        self.scroll.setStyleSheet("""
            QScrollArea{
                border:none;
                background:#1E1E1E;
            }
        """)


        # Input
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText(
            "Type your message here..."
        )


        # Buttons
        self.send_button = QPushButton(
            "Send"
        )

        self.voice_button = QPushButton(
            "🎤"
        )

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

        bottom_layout.addWidget(
            self.input_box
        )

        bottom_layout.addWidget(
            self.voice_button
        )

        bottom_layout.addWidget(
            self.send_button
        )


        # Assemble
        layout.addWidget(title)
        layout.addWidget(
            self.voice_status
        )

        layout.addWidget(
            self.scroll
        )

        layout.addLayout(
            bottom_layout
        )


        self.setLayout(layout)


        # Events
        self.send_button.clicked.connect(
            self.send_message
        )

        self.input_box.returnPressed.connect(
            self.send_message
        )


        self.show_welcome_message()


        # Wake Word Thread
        self.voice_manager = VoiceManager()

        self.voice_manager.wake_detected.connect(
            self.on_wake_detected
        )

        self.voice_manager.command_detected.connect(
            self.voice_finished
        )

        self.voice_manager.start()



    def send_message(self):

        command = self.input_box.text().strip()

        if not command:
            return


        self.current_command = command


        self.chat_container.add_message(
            "🧑 You",
            command,
            True
        )


        self.scroll_to_bottom()


        if command != "__WAKE__":

            self.chat_container.add_message(
                "🤖 JARVIS",
                "Typing...",
                False
            )


        self.scroll_to_bottom()

        self.input_box.clear()


        QTimer.singleShot(
            CHAT_TYPING_DELAY,
            self.generate_response
        )



    def generate_response(self):

        if self.current_command == "__WAKE__":

            speech_manager.say(
                "Yes?"
            )


            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            app_state.last_active = time.time()


            self.chat_container.add_message(
                "🤖 JARVIS",
                "Yes?",
                False
            )

            self.scroll_to_bottom()

            return



        # Thinking
        app_state.state_machine.change(
            AssistantState.THINKING
        )


        response = self.brain.process(
            self.current_command
        )
        print("Brain response:", response)


        if not response:

            response = (
                "Sorry, I couldn't process that request."
            )


        self.chat_container.add_message(
            "🤖 JARVIS",
            response,
            False
        )


        self.scroll_to_bottom()



        # Speaking
        
        speech_manager.say(response)
        app_state.last_active = time.time()



    def show_welcome_message(self):

        self.chat_container.add_message(
            "🤖 JARVIS",
            "Hello Anas! 👋\nWelcome back.\nHow can I help you today?",
            False
        )

        self.scroll_to_bottom()


    def voice_finished(self, text):

        app_state.last_active = time.time()
        self.animation_timer.stop()

        self.voice_button.setEnabled(
            True
        )


        self.voice_status.setText(
            "Ready"
        )


        if not text:

            self.chat_container.add_message(
                "🤖 JARVIS",
                "Sorry, I couldn't hear you.",
                False
            )

            self.scroll_to_bottom()

            return



        self.input_box.setText(
            text
        )


        self.send_message()


        app_state.state_machine.change(
            AssistantState.AWAKE
        )


        



    def on_wake_detected(self, command):

        app_state.state_machine.change(
            AssistantState.AWAKE
        )
    
        app_state.last_active = time.time()
    
        speech_manager.say("Yes?")
    
        if command:
            self.input_box.setText(command)
            self.send_message()


    def scroll_to_bottom(self):

        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )



    def animate_listening(self):

        dots = "." * (
            (self.animation_step % 3) + 1
        )


        self.voice_status.setText(
            f"🎙️ Listening{dots}"
        )


        self.animation_step += 1



    def check_sleep_timeout(self):

        elapsed = (
            time.time()
            -
            app_state.last_active
        )


        if not app_state.state_machine.is_awake():
            return



        if elapsed > AWAKE_TIMEOUT:


            app_state.state_machine.change(
                AssistantState.SLEEPING
            )


            self.voice_status.setText(
                "😴 Sleeping"
            )


            self.chat_container.add_message(
                "🤖 JARVIS",
                "Going back to sleep.",
                False
            )


            self.scroll_to_bottom()

    
    def closeEvent(self, event):

        if hasattr(self, "voice_manager"):
            self.voice_manager.stop()
            self.voice_manager.wait()

        event.accept()