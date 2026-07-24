from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
)

from gui.sidebar import Sidebar
from core.system import System


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.setWindowTitle("JARVIS AI 4.0")
        self.resize(1200, 700)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = Sidebar()

        # Content Area
        content = QWidget()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.setSpacing(20)

        # Title
        title = QLabel("🤖 JARVIS AI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("Powered by Python & AI")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.start_button = QPushButton("Start JARVIS")
        self.exit_button = QPushButton("Exit")

        self.start_button.setFixedWidth(220)
        self.exit_button.setFixedWidth(220)

        # Add widgets to content layout
        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addWidget(self.start_button)
        content_layout.addWidget(self.exit_button)

        content.setLayout(content_layout)

        # Add sidebar and content to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        central_widget.setLayout(main_layout)

        # Events
        self.start_button.clicked.connect(self.start_jarvis)
        self.exit_button.clicked.connect(self.close)

    def start_jarvis(self):
        info = (
            f"Operating System: {System.operating_system()}\n"
            f"Processor: {System.processor()}\n"
            f"Python Version: {System.python_version()}\n"
            f"RAM: {System.total_ram()} GB"
        )

        QMessageBox.information(
            self,
            "System Information",
            info,
        )