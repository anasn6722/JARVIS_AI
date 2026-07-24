from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)

from gui.widgets.info_card import InfoCard
from core.system import System


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Dashboard Title
        title = QLabel("🏠 Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)

        # Grid Layout
        grid = QGridLayout()

        # Cards
        self.cpu_card = InfoCard(
            "💻 CPU Usage",
            f"{System.cpu_usage()}%"
        )

        self.ram_card = InfoCard(
            "🧠 RAM Used",
            f"{System.ram_used()} GB"
        )

        self.ai_card = InfoCard(
            "🤖 AI",
            "Online"
        )

        self.voice_card = InfoCard(
            "🎤 Voice",
            "Ready"
        )

        # Add Cards
        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.ai_card, 1, 0)
        grid.addWidget(self.voice_card, 1, 1)

        # Main Layout
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(grid)
        layout.addStretch()

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)

    def update_system_info(self):
        """Update CPU and RAM information every second."""
        self.cpu_card.update_value(
            f"{System.cpu_usage()}%"
        )

        self.ram_card.update_value(
            f"{System.ram_used()} GB"
        )