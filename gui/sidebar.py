from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.dashboard_btn = QPushButton("🏠 Dashboard")
        self.chat_btn = QPushButton("💬 Chat")
        self.voice_btn = QPushButton("🎤 Voice")
        self.memory_btn = QPushButton("🧠 Memory")
        self.settings_btn = QPushButton("⚙ Settings")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.chat_btn)
        layout.addWidget(self.voice_btn)
        layout.addWidget(self.memory_btn)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        self.setLayout(layout)

        self.setFixedWidth(220)