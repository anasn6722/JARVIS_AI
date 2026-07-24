from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)

from gui.widgets.info_card import InfoCard


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # Dashboard Title
        title = QLabel("🏠 Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:white;
        """)

        # Grid Layout for Cards
        grid = QGridLayout()
        grid.setSpacing(20)

        # Create Cards
        cpu_card = InfoCard("💻 CPU Usage", "0%")
        ram_card = InfoCard("🧠 RAM Usage", "0 GB")
        ai_card = InfoCard("🤖 AI Status", "Ready")
        voice_card = InfoCard("🎤 Voice", "Offline")

        # Add Cards
        grid.addWidget(cpu_card, 0, 0)
        grid.addWidget(ram_card, 0, 1)
        grid.addWidget(ai_card, 1, 0)
        grid.addWidget(voice_card, 1, 1)

        # Assemble Layout
        main_layout.addWidget(title)
        main_layout.addSpacing(20)
        main_layout.addLayout(grid)
        main_layout.addStretch()

        self.setLayout(main_layout)