from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QKeySequence,
    QShortcut,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gui.pages.chat_page import ChatPage
from gui.pages.dashboard_page import DashboardPage
from gui.pages.memory_page import MemoryPage
from gui.pages.settings_page import SettingsPage
from gui.pages.voice_page import VoicePage
from gui.sidebar import Sidebar
from gui.widgets.hud_overlay import HudOverlay
from gui.widgets.page_transition import (
    PageTransition,
)


class MainWindow(QMainWindow):
    """Main JARVIS HUD window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "JARVIS AI 4.0"
        )

        self.resize(
            1400,
            850,
        )

        self.setMinimumSize(
            1100,
            700,
        )

        self.immersive_mode = False

        # =====================================================
        # CENTRAL WIDGET
        # =====================================================

        central_widget = QWidget()

        central_widget.setObjectName(
            "hudRoot"
        )

        self.setCentralWidget(
            central_widget
        )

        # =====================================================
        # HUD OVERLAY
        # =====================================================

        self.hud_overlay = HudOverlay(
            central_widget
        )

        self.hud_overlay.setGeometry(
            central_widget.rect()
        )

        self.hud_overlay.raise_()

        # =====================================================
        # ROOT LAYOUT
        # =====================================================

        root_layout = QVBoxLayout(
            central_widget
        )

        root_layout.setContentsMargins(
            18,
            14,
            18,
            18,
        )

        root_layout.setSpacing(
            12
        )

        # =====================================================
        # TOP HUD
        # =====================================================

        self.top_bar = (
            self._create_top_bar()
        )

        root_layout.addWidget(
            self.top_bar
        )

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        content_widget = QWidget()

        content_layout = QHBoxLayout(
            content_widget
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(
            12
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar = Sidebar()

        # =====================================================
        # PAGES
        # =====================================================

        self.pages = QStackedWidget()

        self.dashboard_page = (
            DashboardPage()
        )

        self.chat_page = (
            ChatPage()
        )

        self.voice_page = (
            VoicePage()
        )

        self.memory_page = (
            MemoryPage()
        )

        self.settings_page = (
            SettingsPage()
        )

        self.pages.addWidget(
            self.dashboard_page
        )

        self.pages.addWidget(
            self.chat_page
        )

        self.pages.addWidget(
            self.voice_page
        )

        self.pages.addWidget(
            self.memory_page
        )

        self.pages.addWidget(
            self.settings_page
        )

        self.page_transitions = [
            PageTransition(
                self.dashboard_page
            ),
            PageTransition(
                self.chat_page
            ),
            PageTransition(
                self.voice_page
            ),
            PageTransition(
                self.memory_page
            ),
            PageTransition(
                self.settings_page
            ),
        ]

        # =====================================================
        # CONTENT
        # =====================================================

        content_layout.addWidget(
            self.sidebar
        )

        content_layout.addWidget(
            self.pages,
            1,
        )

        root_layout.addWidget(
            content_widget,
            1,
        )

        # =====================================================
        # INITIAL PAGE
        # =====================================================

        self.pages.setCurrentIndex(
            0
        )
        
        self.page_transitions[
            0
        ].play(
            0
        )

        self.sidebar.set_active(
            self.sidebar.dashboard_btn
        )

        # =====================================================
        # NAVIGATION
        # =====================================================

        self.sidebar.dashboard_btn.clicked.connect(
            lambda: self._show_page(
                0,
                self.sidebar.dashboard_btn,
            )
        )

        self.sidebar.chat_btn.clicked.connect(
            lambda: self._show_page(
                1,
                self.sidebar.chat_btn,
            )
        )

        self.sidebar.voice_btn.clicked.connect(
            lambda: self._show_page(
                2,
                self.sidebar.voice_btn,
            )
        )

        self.sidebar.memory_btn.clicked.connect(
            lambda: self._show_page(
                3,
                self.sidebar.memory_btn,
            )
        )

        self.sidebar.settings_btn.clicked.connect(
            lambda: self._show_page(
                4,
                self.sidebar.settings_btn,
            )
        )

        # =====================================================
        # F11 SHORTCUT
        # =====================================================

        self.fullscreen_shortcut = QShortcut(
            QKeySequence("F11"),
            self,
        )

        self.fullscreen_shortcut.activated.connect(
            self.toggle_immersive_mode
        )

    # =========================================================
    # TOP HUD
    # =========================================================

    def _create_top_bar(self):
        frame = QFrame()

        frame.setProperty(
            "class",
            "hudPanel",
        )

        frame.setFixedHeight(
            72
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            20,
            10,
            14,
            10,
        )

        # =====================================================
        # LEFT
        # =====================================================

        left_layout = QVBoxLayout()

        left_layout.setSpacing(
            0
        )

        title = QLabel(
            "J A R V I S"
        )

        title.setProperty(
            "class",
            "hudTitle",
        )

        subtitle = QLabel(
            "JUST A RATHER VERY INTELLIGENT SYSTEM"
        )

        subtitle.setProperty(
            "class",
            "hudSubtitle",
        )

        left_layout.addWidget(
            title
        )

        left_layout.addWidget(
            subtitle
        )

        # =====================================================
        # CENTER
        # =====================================================

        center_label = QLabel(
            "SYSTEM // ONLINE"
        )

        center_label.setProperty(
            "class",
            "statusOnline",
        )

        center_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # =====================================================
        # IMMERSIVE BUTTON
        # =====================================================

        self.immersive_button = QPushButton(
            "IMMERSIVE"
        )

        self.immersive_button.setFixedWidth(
            105
        )

        self.immersive_button.clicked.connect(
            self.toggle_immersive_mode
        )

        # =====================================================
        # RIGHT
        # =====================================================

        self.core_status_label = QLabel(
            "CORE: STABLE"
        )

        self.core_status_label.setProperty(
            "class",
            "statusOnline",
        )

        self.core_status_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addLayout(
            left_layout
        )

        layout.addStretch(
            1
        )

        layout.addWidget(
            center_label
        )

        layout.addStretch(
            1
        )

        layout.addWidget(
            self.core_status_label
        )

        layout.addWidget(
            self.immersive_button
        )

        return frame

    # =========================================================
    # PAGE NAVIGATION
    # =========================================================

    def _show_page(
        self,
        index,
        button,
    ):
        self.pages.setCurrentIndex(
            index
        )

        self.sidebar.set_active(
            button
        )

        self.page_transitions[
            index
        ].play()

    # =========================================================
    # IMMERSIVE MODE
    # =========================================================

    def toggle_immersive_mode(self):
        """Toggle between normal and full-screen HUD mode."""

        if self.immersive_mode:
            self.exit_immersive_mode()
        else:
            self.enter_immersive_mode()

    def enter_immersive_mode(self):
        self.immersive_mode = True

        self.immersive_button.setText(
            "EXIT HUD"
        )

        self.core_status_label.setText(
            "CORE: IMMERSIVE"
        )

        self.showFullScreen()

    def exit_immersive_mode(self):
        self.immersive_mode = False

        self.immersive_button.setText(
            "IMMERSIVE"
        )

        self.core_status_label.setText(
            "CORE: STABLE"
        )

        self.showNormal()

    # =========================================================
    # RESIZE
    # =========================================================
    
    def resizeEvent(self, event):
        super().resizeEvent(
            event
        )
    
        if hasattr(
            self,
            "hud_overlay",
        ):
            self.hud_overlay.setGeometry(
                self.centralWidget().rect()
            )
    
            self.hud_overlay.raise_()

    # =========================================================
    # CLOSE
    # =========================================================

    def closeEvent(self, event):
        """Stop voice resources before closing."""

        if hasattr(
            self.chat_page,
            "voice_manager",
        ):
            self.chat_page.voice_manager.stop()

            self.chat_page.voice_manager.wait()

        event.accept()