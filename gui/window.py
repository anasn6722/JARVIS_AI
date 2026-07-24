from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from gui.sidebar import Sidebar

from gui.pages.dashboard_page import DashboardPage
from gui.pages.chat_page import ChatPage
from gui.pages.voice_page import VoicePage
from gui.pages.memory_page import MemoryPage
from gui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS AI 4.0")
        self.resize(1200, 700)

        # -----------------------
        # Central Widget
        # -----------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # -----------------------
        # Main Layout
        # -----------------------

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # -----------------------
        # Sidebar
        # -----------------------

        self.sidebar = Sidebar()

        # -----------------------
        # Pages
        # -----------------------

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.chat_page = ChatPage()
        self.voice_page = VoicePage()
        self.memory_page = MemoryPage()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.chat_page)
        self.pages.addWidget(self.voice_page)
        self.pages.addWidget(self.memory_page)
        self.pages.addWidget(self.settings_page)

        # -----------------------
        # Layout
        # -----------------------

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        # Show Dashboard First
        self.pages.setCurrentIndex(0)