from PySide6.QtCore import Qt
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

        title = QLabel("🏠 Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:white;
        """)

        grid = QGridLayout()

        cpu = InfoCard(
            "💻 CPU Usage",
            f"{System.cpu_usage()}%"
        )

        ram = InfoCard(
            "🧠 RAM Used",
            f"{System.ram_used()} GB"
        )

        ai = InfoCard(
            "🤖 AI",
            "Online"
        )

        voice = InfoCard(
            "🎤 Voice",
            "Ready"
        )

        grid.addWidget(cpu, 0, 0)
        grid.addWidget(ram, 0, 1)
        grid.addWidget(ai, 1, 0)
        grid.addWidget(voice, 1, 1)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addLayout(grid)
        layout.addStretch()

        self.setLayout(layout)