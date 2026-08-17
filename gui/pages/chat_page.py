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
from gui.widgets.command_console import CommandConsole
from voice.voice_manager import VoiceManager


class ChatPage(QWidget):
    """JARVIS holographic command console."""

    def __init__(self):
        super().__init__()

        self.brain = Brain()

        self.current_command = ""

        app_state.state_machine.change(
            AssistantState.SLEEPING
        )

        # =====================================================
        # PAGE STYLE
        # =====================================================

        self.setObjectName(
            "chatPage"
        )

        self.setStyleSheet(
            """
            QWidget#chatPage {
                background: transparent;
            }

            QLabel#chatTitle {
                color: #7cecff;
                font-size: 27px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#chatSubtitle {
                color: #4f8f9b;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#voiceStatus {
                color: #73f7dc;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLineEdit#commandInput {
                background-color: rgba(4, 20, 26, 240);
                color: #d7fbff;
                border: 1px solid #1a5c68;
                border-radius: 9px;
                padding: 11px 14px;
                font-family: Consolas;
                font-size: 12px;
            }

            QLineEdit#commandInput:focus {
                border: 1px solid #43d9ea;
            }

            QPushButton#sendButton {
                background-color: #0b4f5c;
                color: #cfffff;
                border: 1px solid #35bccc;
                border-radius: 9px;
                padding: 10px 20px;
                font-weight: 700;
            }

            QPushButton#sendButton:hover {
                background-color: #106d7b;
            }

            QPushButton#voiceButton {
                background-color: #07434c;
                color: #8df7ff;
                border: 1px solid #31c4d4;
                border-radius: 9px;
                font-size: 18px;
            }

            QPushButton#voiceButton:hover {
                background-color: #0c6370;
            }

            QScrollArea#chatScroll {
                border: 1px solid #123e48;
                border-radius: 10px;
                background: rgba(2, 11, 15, 190);
            }
            """
        )

        # =====================================================
        # TIMERS
        # =====================================================

        self.animation_timer = QTimer(
            self
        )

        self.animation_timer.timeout.connect(
            self.animate_listening
        )

        self.animation_step = 0

        self.sleep_timer = QTimer(
            self
        )

        self.sleep_timer.timeout.connect(
            self.check_sleep_timeout
        )

        self.sleep_timer.start(
            1000
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        layout.setSpacing(8)

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "JARVIS // COMMAND CONSOLE"
        )

        title.setObjectName(
            "chatTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "NATURAL LANGUAGE INTERFACE // "
            "VOICE + TEXT // DESKTOP CONTROL"
        )

        subtitle.setObjectName(
            "chatSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.voice_status = QLabel(
            "● READY"
        )

        self.voice_status.setObjectName(
            "voiceStatus"
        )

        self.voice_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.voice_status
        )

        # =====================================================
        # COMMAND CONSOLE
        # =====================================================

        self.command_console = (
            CommandConsole()
        )

        layout.addWidget(
            self.command_console
        )

        # =====================================================
        # CHAT
        # =====================================================

        self.chat_container = (
            ChatContainer()
        )

        self.scroll = QScrollArea()

        self.scroll.setObjectName(
            "chatScroll"
        )

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setWidget(
            self.chat_container
        )

        layout.addWidget(
            self.scroll,
            1,
        )

        # =====================================================
        # INPUT
        # =====================================================

        self.input_box = QLineEdit()

        self.input_box.setObjectName(
            "commandInput"
        )

        self.input_box.setPlaceholderText(
            "Enter JARVIS command..."
        )

        self.send_button = QPushButton(
            "EXECUTE"
        )

        self.send_button.setObjectName(
            "sendButton"
        )

        self.voice_button = QPushButton(
            "🎤"
        )

        self.voice_button.setObjectName(
            "voiceButton"
        )

        self.voice_button.setFixedWidth(
            58
        )

        bottom_layout = QHBoxLayout()

        bottom_layout.setSpacing(
            8
        )

        bottom_layout.addWidget(
            self.input_box
        )

        bottom_layout.addWidget(
            self.voice_button
        )

        bottom_layout.addWidget(
            self.send_button
        )

        layout.addLayout(
            bottom_layout
        )

        # =====================================================
        # CONNECTIONS
        # =====================================================

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input_box.returnPressed.connect(
            self.send_message
        )

        # =====================================================
        # WELCOME
        # =====================================================

        self.show_welcome_message()

        # =====================================================
        # VOICE MANAGER
        # =====================================================

        self.voice_manager = VoiceManager()

        self.voice_manager.wake_detected.connect(
            self.on_wake_detected
        )

        self.voice_manager.command_detected.connect(
            self.voice_finished
        )

        self.voice_manager.start()

    # =========================================================
    # SEND
    # =========================================================

    def send_message(self):
        command = (
            self.input_box.text()
            .strip()
        )

        if not command:
            return

        self.current_command = command

        self.command_console.show_command(
            command
        )

        self.command_console.show_processing()

        self.chat_container.add_message(
            "🧑 You",
            command,
            True,
        )

        self.chat_container.add_message(
            "🤖 JARVIS",
            "Processing...",
            False,
        )

        self.scroll_to_bottom()

        self.input_box.clear()

        QTimer.singleShot(
            CHAT_TYPING_DELAY,
            self.generate_response,
        )

    # =========================================================
    # GENERATE RESPONSE
    # =========================================================

    def generate_response(self):
        if (
            self.current_command
            == "__WAKE__"
        ):

            response = "Yes?"

            speech_manager.say(
                response
            )

            app_state.state_machine.change(
                AssistantState.AWAKE
            )

            app_state.last_active = (
                time.time()
            )

            self.command_console.show_response(
                response
            )

            self.chat_container.add_message(
                "🤖 JARVIS",
                response,
                False,
            )

            self.scroll_to_bottom()

            return

        # =====================================================
        # THINKING
        # =====================================================

        app_state.state_machine.change(
            AssistantState.THINKING
        )

        self.voice_status.setText(
            "● THINKING"
        )

        try:
            response = self.brain.process(
                self.current_command
            )

            print(
                "Brain response:",
                response,
            )

        except Exception as error:
            print(
                "Brain error:",
                error,
            )

            response = (
                "Sorry, I couldn't "
                "process that request."
            )

            self.command_console.show_error(
                response
            )

        if not response:
            response = (
                "Sorry, I couldn't "
                "process that request."
            )

        # =====================================================
        # COMMAND CONSOLE
        # =====================================================

        self.command_console.show_response(
            response
        )

        # =====================================================
        # CHAT
        # =====================================================

        self.chat_container.add_message(
            "🤖 JARVIS",
            response,
            False,
        )

        self.scroll_to_bottom()

        # =====================================================
        # SPEAK
        # =====================================================

        self.voice_status.setText(
            "● SPEAKING"
        )

        speech_manager.say(
            response
        )

        app_state.last_active = (
            time.time()
        )

    # =========================================================
    # WELCOME
    # =========================================================

    def show_welcome_message(self):
        response = (
            "Hello Anas! 👋\n"
            "Welcome back.\n"
            "How can I help you today?"
        )

        self.command_console.show_response(
            response
        )

        self.chat_container.add_message(
            "🤖 JARVIS",
            response,
            False,
        )

        self.scroll_to_bottom()

    # =========================================================
    # VOICE COMMAND
    # =========================================================

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
        
            app_state.state_machine.change(
                AssistantState.AWAKE
            )
    
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

    # =========================================================
    # WAKE WORD
    # =========================================================

    def on_wake_detected(
        self,
        command,
    ):
        app_state.state_machine.change(
            AssistantState.AWAKE
        )

        app_state.last_active = (
            time.time()
        )

        speech_manager.say(
            "Yes?"
        )

        if command:
            self.input_box.setText(
                command
            )

            self.send_message()

    # =========================================================
    # SCROLL
    # =========================================================

    def scroll_to_bottom(self):
        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

    # =========================================================
    # LISTENING ANIMATION
    # =========================================================

    def animate_listening(self):
        dots = "." * (
            (
                self.animation_step
                % 3
            )
            + 1
        )

        self.voice_status.setText(
            f"● LISTENING{dots}"
        )

        self.animation_step += 1

    # =========================================================
    # SLEEP
    # =========================================================

    def check_sleep_timeout(self):
        elapsed = (
            time.time()
            - app_state.last_active
        )

        if not app_state.state_machine.is_awake():
            return

        if elapsed > AWAKE_TIMEOUT:

            app_state.state_machine.change(
                AssistantState.SLEEPING
            )

            self.voice_status.setText(
                "● SLEEPING"
            )

            message = (
                "Going back to sleep."
            )

            self.command_console.show_response(
                message
            )

            self.chat_container.add_message(
                "🤖 JARVIS",
                message,
                False,
            )

            self.scroll_to_bottom()

    # =========================================================
    # CLOSE
    # =========================================================

    def closeEvent(self, event):
        if hasattr(
            self,
            "voice_manager",
        ):
            self.voice_manager.stop()
            self.voice_manager.wait()

        event.accept()