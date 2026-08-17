from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):
    """Holographic JARVIS navigation panel."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "jarvisSidebar"
        )

        self.setFixedWidth(165)

        self.setStyleSheet(
            """
            QWidget#jarvisSidebar {
                background-color: rgba(4, 15, 20, 235);
                border: 1px solid #124653;
                border-radius: 14px;
            }

            QLabel#brand {
                color: #7cecff;
                font-size: 21px;
                font-weight: 700;
                letter-spacing: 4px;
            }

            QLabel#brandSubtitle {
                color: #4d8994;
                font-size: 8px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#sectionLabel {
                color: #396c76;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 2px;
                padding-top: 8px;
                padding-bottom: 3px;
            }

            QPushButton.navButton {
                text-align: left;
                background-color: transparent;
                color: #6fa3ac;
                border: 1px solid transparent;
                border-radius: 8px;
                padding: 8px 8px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0px;
            }

            QPushButton.navButton:hover {
                background-color: rgba(17, 54, 63, 180);
                color: #bdf8ff;
                border: 1px solid #1d6470;
            }

            QPushButton.navButton:checked {
                background-color: rgba(13, 66, 77, 210);
                color: #8ff7ff;
                border: 1px solid #37c8da;
            }

            QFrame#systemPanel {
                background-color: rgba(3, 22, 27, 220);
                border: 1px solid #12434d;
                border-radius: 9px;
            }

            QLabel#systemTitle {
                color: #4d8994;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#systemStatus {
                color: #73f7dc;
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#version {
                color: #315861;
                font-size: 8px;
                font-family: Consolas;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            14,
            10,
            12,
        )

        layout.setSpacing(
            6
        )

        # =====================================================
        # BRAND
        # =====================================================

        brand = QLabel(
            "JARVIS"
        )

        brand.setObjectName(
            "brand"
        )

        brand.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            brand
        )

        subtitle = QLabel(
            "COMMAND INTERFACE"
        )

        subtitle.setObjectName(
            "brandSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            14
        )

        # =====================================================
        # NAVIGATION LABEL
        # =====================================================

        navigation_label = QLabel(
            "NAVIGATION"
        )

        navigation_label.setObjectName(
            "sectionLabel"
        )

        layout.addWidget(
            navigation_label
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.dashboard_btn = self._create_button(
            "◉   COMMAND CENTER"
        )

        self.chat_btn = self._create_button(
            "◇   CHAT CONSOLE"
        )

        self.voice_btn = self._create_button(
            "◇   VOICE INTERFACE"
        )

        self.memory_btn = self._create_button(
            "◇   MEMORY CORE"
        )

        self.settings_btn = self._create_button(
            "◇   SYSTEM SETTINGS"
        )

        layout.addWidget(
            self.dashboard_btn
        )

        layout.addWidget(
            self.chat_btn
        )

        layout.addWidget(
            self.voice_btn
        )

        layout.addWidget(
            self.memory_btn
        )

        layout.addWidget(
            self.settings_btn
        )

        layout.addStretch()

        # =====================================================
        # SYSTEM PANEL
        # =====================================================

        system_panel = QFrame()

        system_panel.setObjectName(
            "systemPanel"
        )

        system_layout = QVBoxLayout(
            system_panel
        )

        system_layout.setContentsMargins(
            10,
            9,
            10,
            9,
        )

        system_layout.setSpacing(
            3
        )

        system_title = QLabel(
            "SYSTEM STATUS"
        )

        system_title.setObjectName(
            "systemTitle"
        )

        system_status = QLabel(
            "● ONLINE"
        )

        system_status.setObjectName(
            "systemStatus"
        )

        system_layout.addWidget(
            system_title
        )

        system_layout.addWidget(
            system_status
        )

        layout.addWidget(
            system_panel
        )

        # =====================================================
        # VERSION
        # =====================================================

        version = QLabel(
            "JARVIS AI 4.0"
        )

        version.setObjectName(
            "version"
        )

        version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(
            8
        )

        layout.addWidget(
            version
        )

        # =====================================================
        # GROUP
        # =====================================================

        self.buttons = (
            self.dashboard_btn,
            self.chat_btn,
            self.voice_btn,
            self.memory_btn,
            self.settings_btn,
        )

        self._configure_exclusive_buttons()

        # Dashboard active by default.
        self.set_active(
            self.dashboard_btn
        )

    # =========================================================
    # CREATE BUTTON
    # =========================================================

    @staticmethod
    def _create_button(text):
        button = QPushButton(
            text
        )

        button.setObjectName(
            "navButton"
        )

        button.setProperty(
            "class",
            "navButton",
        )

        button.setCheckable(
            True
        )

        button.setMinimumHeight(
            34
        )

        return button

    # =========================================================
    # EXCLUSIVE BUTTONS
    # =========================================================

    def _configure_exclusive_buttons(self):
        for button in self.buttons:
            button.clicked.connect(
                lambda checked=False,
                current=button:
                self.set_active(current)
            )

    # =========================================================
    # ACTIVE BUTTON
    # =========================================================

    from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):
    """Holographic JARVIS navigation panel."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "jarvisSidebar"
        )

        self.setFixedWidth(165)

        self.setStyleSheet(
            """
            QWidget#jarvisSidebar {
                background-color: rgba(4, 15, 20, 235);
                border: 1px solid #124653;
                border-radius: 14px;
            }

            QLabel#brand {
                color: #7cecff;
                font-size: 21px;
                font-weight: 700;
                letter-spacing: 4px;
            }

            QLabel#brandSubtitle {
                color: #4d8994;
                font-size: 8px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#sectionLabel {
                color: #396c76;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 2px;
                padding-top: 8px;
                padding-bottom: 3px;
            }

            QPushButton.navButton {
                text-align: left;
                background-color: transparent;
                color: #6fa3ac;
                border: 1px solid transparent;
                border-radius: 8px;
                padding: 8px 8px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0px;
            }

            QPushButton.navButton:hover {
                background-color: rgba(17, 54, 63, 180);
                color: #bdf8ff;
                border: 1px solid #1d6470;
            }

            QPushButton.navButton:checked {
                background-color: rgba(13, 66, 77, 210);
                color: #8ff7ff;
                border: 1px solid #37c8da;
            }

            QFrame#systemPanel {
                background-color: rgba(3, 22, 27, 220);
                border: 1px solid #12434d;
                border-radius: 9px;
            }

            QLabel#systemTitle {
                color: #4d8994;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#systemStatus {
                color: #73f7dc;
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#version {
                color: #315861;
                font-size: 8px;
                font-family: Consolas;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            14,
            10,
            12,
        )

        layout.setSpacing(
            6
        )

        # =====================================================
        # BRAND
        # =====================================================

        brand = QLabel(
            "JARVIS"
        )

        brand.setObjectName(
            "brand"
        )

        brand.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            brand
        )

        subtitle = QLabel(
            "COMMAND INTERFACE"
        )

        subtitle.setObjectName(
            "brandSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            14
        )

        # =====================================================
        # NAVIGATION LABEL
        # =====================================================

        navigation_label = QLabel(
            "NAVIGATION"
        )

        navigation_label.setObjectName(
            "sectionLabel"
        )

        layout.addWidget(
            navigation_label
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.dashboard_btn = self._create_button(
            "◉   COMMAND CENTER"
        )

        self.chat_btn = self._create_button(
            "◇   CHAT CONSOLE"
        )

        self.voice_btn = self._create_button(
            "◇   VOICE INTERFACE"
        )

        self.memory_btn = self._create_button(
            "◇   MEMORY CORE"
        )

        self.settings_btn = self._create_button(
            "◇   SYSTEM SETTINGS"
        )

        layout.addWidget(
            self.dashboard_btn
        )

        layout.addWidget(
            self.chat_btn
        )

        layout.addWidget(
            self.voice_btn
        )

        layout.addWidget(
            self.memory_btn
        )

        layout.addWidget(
            self.settings_btn
        )

        layout.addStretch()

        # =====================================================
        # SYSTEM PANEL
        # =====================================================

        system_panel = QFrame()

        system_panel.setObjectName(
            "systemPanel"
        )

        system_layout = QVBoxLayout(
            system_panel
        )

        system_layout.setContentsMargins(
            10,
            9,
            10,
            9,
        )

        system_layout.setSpacing(
            3
        )

        system_title = QLabel(
            "SYSTEM STATUS"
        )

        system_title.setObjectName(
            "systemTitle"
        )

        system_status = QLabel(
            "● ONLINE"
        )

        system_status.setObjectName(
            "systemStatus"
        )

        system_layout.addWidget(
            system_title
        )

        system_layout.addWidget(
            system_status
        )

        layout.addWidget(
            system_panel
        )

        # =====================================================
        # VERSION
        # =====================================================

        version = QLabel(
            "JARVIS AI 4.0"
        )

        version.setObjectName(
            "version"
        )

        version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(
            8
        )

        layout.addWidget(
            version
        )

        # =====================================================
        # GROUP
        # =====================================================

        self.buttons = (
            self.dashboard_btn,
            self.chat_btn,
            self.voice_btn,
            self.memory_btn,
            self.settings_btn,
        )

        self._configure_exclusive_buttons()

        # Dashboard active by default.
        self.set_active(
            self.dashboard_btn
        )

    # =========================================================
    # CREATE BUTTON
    # =========================================================

    @staticmethod
    def _create_button(text):
        button = QPushButton(
            text
        )

        button.setObjectName(
            "navButton"
        )

        button.setProperty(
            "class",
            "navButton",
        )

        button.setCheckable(
            True
        )

        button.setMinimumHeight(
            34
        )

        return button

    # =========================================================
    # EXCLUSIVE BUTTONS
    # =========================================================

    def _configure_exclusive_buttons(self):
        for button in self.buttons:
            button.clicked.connect(
                lambda checked=False,
                current=button:
                self.set_active(current)
            )

    # =========================================================
    # ACTIVE BUTTON
    # =========================================================

    def set_active(self, button):
        for item in self.buttons:
            item.setChecked(
                item is button
            )
    
            item.style().unpolish(
                item
            )
    
            item.style().polish(
                item
            )
    
            item.update()