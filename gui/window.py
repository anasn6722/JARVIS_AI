from PySide6.QtCore import Qt
from core.system import System
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        # ----------------------------
        # Window Settings
        # ----------------------------
        self.setWindowTitle("JARVIS AI 4.0")
        self.resize(1200, 700)

        # ----------------------------
        # Central Widget
        # ----------------------------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ----------------------------
        # Main Layout
        # ----------------------------
        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.setSpacing(20)

        # ----------------------------
        # Title
        # ----------------------------
        title = QLabel("🤖 JARVIS AI")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----------------------------
        # Subtitle
        # ----------------------------
        subtitle = QLabel(
            "Powered by Python & AI"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ----------------------------
        # Buttons
        # ----------------------------
        self.start_button = QPushButton(
            "Start JARVIS"
        )

        self.exit_button = QPushButton(
            "Exit"
        )

        self.start_button.setFixedWidth(220)
        self.exit_button.setFixedWidth(220)

        # ----------------------------
        # Add Widgets
        # ----------------------------
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.start_button)
        layout.addWidget(self.exit_button)

        central_widget.setLayout(layout)

        # ----------------------------
        # Events
        # ----------------------------
        self.start_button.clicked.connect(
            self.start_jarvis
        )

        self.exit_button.clicked.connect(
            self.close
        )

    def start_jarvis(self):
     info = (
        f"Operating System: {System.operating_system()}\n"
        f"Processor: {System.processor()}\n"
        f"Python: {System.python_version()}\n"
        f"RAM: {System.total_ram()} GB"
     )

     QMessageBox.information(
        self,
        "System Information",
        info
    )