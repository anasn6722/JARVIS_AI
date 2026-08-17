from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from voice.language_manager import language_manager


class SettingsPage(QWidget):
    """JARVIS system settings HUD."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "settingsPage"
        )

        self.setStyleSheet(
            """
            QWidget#settingsPage {
                background: transparent;
            }

            QLabel#settingsTitle {
                color: #7cecff;
                font-size: 27px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#settingsSubtitle {
                color: #4f8f9b;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QFrame.settingsCard {
                background-color: rgba(5, 18, 24, 238);
                border: 1px solid #175360;
                border-radius: 14px;
            }

            QLabel.sectionTitle {
                color: #7cecff;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel.settingName {
                color: #9edbe4;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel.settingDescription {
                color: #4f8f9b;
                font-size: 9px;
            }

            QLabel.valueLabel {
                color: #73f7dc;
                font-size: 10px;
                font-weight: 700;
            }

            QComboBox {
                background-color: #07151b;
                color: #d9faff;
                border: 1px solid #185461;
                border-radius: 8px;
                padding: 7px 10px;
                min-width: 150px;
            }

            QComboBox:hover {
                border: 1px solid #35c6da;
            }

            QCheckBox {
                color: #9edbe4;
                font-size: 10px;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #185461;
                background: #07151b;
            }

            QCheckBox::indicator:checked {
                background: #26c6da;
                border: 1px solid #73f7dc;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #12323a;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
                background: #73eaff;
            }

            QSlider::sub-page:horizontal {
                background: #26c6da;
                border-radius: 3px;
            }

            QPushButton.settingsButton {
                background-color: #07151b;
                color: #9eefff;
                border: 1px solid #185461;
                border-radius: 8px;
                padding: 9px 16px;
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton.settingsButton:hover {
                background-color: #0b252d;
                border: 1px solid #35c6da;
            }

            QPushButton.primaryButton {
                background-color: #10343d;
                color: #bdf8ff;
                border: 1px solid #35c6da;
            }
            """
        )

        # =====================================================
        # ROOT
        # =====================================================

        root = QVBoxLayout(self)

        root.setContentsMargins(
            24,
            18,
            24,
            18,
        )

        root.setSpacing(8)

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "SYSTEM SETTINGS"
        )

        title.setObjectName(
            "settingsTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "JARVIS // VOICE // AI // HUD // SYSTEM"
        )

        subtitle.setObjectName(
            "settingsSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addSpacing(10)

        # =====================================================
        # SCROLL AREA
        # =====================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            """
        )

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            8,
        )

        content_layout.setSpacing(
            12
        )

        # =====================================================
        # LANGUAGE & VOICE
        # =====================================================

        language_card = self._create_card()

        language_layout = QVBoxLayout(
            language_card
        )

        language_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        language_layout.setSpacing(
            10
        )

        language_title = QLabel(
            "LANGUAGE & VOICE"
        )

        language_title.setProperty(
            "class",
            "sectionTitle",
        )

        language_layout.addWidget(
            language_title
        )

        # -----------------------------------------------------
        # Primary language
        # -----------------------------------------------------

        language_row = self._setting_row(
            "Primary Language",
            "Language used for speech recognition.",
        )

        self.language_box = QComboBox()

        self.language_box.addItems(
            language_manager.available_languages()
        )

        self.language_box.setCurrentText(
            language_manager.get_primary_language()
        )

        self.language_box.currentTextChanged.connect(
            self._language_changed
        )

        language_row.addWidget(
            self.language_box
        )

        language_layout.addLayout(
            language_row
        )

        # -----------------------------------------------------
        # Auto detection
        # -----------------------------------------------------

        self.auto_language = QCheckBox(
            "Automatically detect spoken language"
        )

        self.auto_language.setChecked(
            language_manager.is_auto_detect()
        )

        self.auto_language.toggled.connect(
            language_manager.set_auto_detect
        )

        language_layout.addWidget(
            self.auto_language
        )

        # -----------------------------------------------------
        # Response language
        # -----------------------------------------------------

        self.same_language = QCheckBox(
            "Respond in the detected language"
        )

        self.same_language.setChecked(
            language_manager.respond_in_detected_language
        )

        self.same_language.toggled.connect(
            language_manager.set_respond_in_detected_language
        )

        language_layout.addWidget(
            self.same_language
        )

        # -----------------------------------------------------
        # Enabled languages
        # -----------------------------------------------------

        enabled_label = QLabel(
            "SUPPORTED LANGUAGES"
        )

        enabled_label.setProperty(
            "class",
            "settingName",
        )

        language_layout.addWidget(
            enabled_label
        )

        self.language_checks = {}

        for language in (
            "English",
            "Urdu",
            "Roman Urdu",
            "Punjabi",
            "Hindi",
        ):

            checkbox = QCheckBox(
                language
            )

            checkbox.setChecked(
                language_manager.is_enabled(
                    language
                )
            )

            checkbox.toggled.connect(
                lambda checked,
                current_language=language:
                self._toggle_language(
                    current_language,
                    checked,
                )
            )

            self.language_checks[
                language
            ] = checkbox

            language_layout.addWidget(
                checkbox
            )

        content_layout.insertWidget(
            0,
            language_card,
        )

        # =====================================================
        # VOICE
        # =====================================================

        voice_card = self._create_card()

        voice_layout = QVBoxLayout(
            voice_card
        )

        voice_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        voice_layout.setSpacing(
            12
        )

        voice_title = QLabel(
            "VOICE SYSTEM"
        )

        voice_title.setProperty(
            "class",
            "sectionTitle",
        )

        voice_layout.addWidget(
            voice_title
        )

        # Wake word
        wake_row = self._setting_row(
            "Wake Word",
            "Phrase used to activate JARVIS.",
        )

        self.wake_word_box = QComboBox()

        self.wake_word_box.addItems(
            [
                "Jarvis",
                "JARVIS",
            ]
        )

        wake_row.addWidget(
            self.wake_word_box
        )

        voice_layout.addLayout(
            wake_row
        )

        # Voice enabled
        self.voice_enabled = QCheckBox(
            "Enable voice interaction"
        )

        self.voice_enabled.setChecked(
            True
        )

        voice_layout.addWidget(
            self.voice_enabled
        )

        # Speech rate
        rate_header = QHBoxLayout()

        rate_name = QLabel(
            "Speech Rate"
        )

        rate_name.setProperty(
            "class",
            "settingName",
        )

        self.rate_value = QLabel(
            "175"
        )

        self.rate_value.setProperty(
            "class",
            "valueLabel",
        )

        rate_header.addWidget(
            rate_name
        )

        rate_header.addStretch()

        rate_header.addWidget(
            self.rate_value
        )

        voice_layout.addLayout(
            rate_header
        )

        self.rate_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.rate_slider.setRange(
            120,
            220,
        )

        self.rate_slider.setValue(
            175
        )

        self.rate_slider.valueChanged.connect(
            lambda value: self.rate_value.setText(
                str(value)
            )
        )

        voice_layout.addWidget(
            self.rate_slider
        )

        # Volume
        volume_header = QHBoxLayout()

        volume_name = QLabel(
            "Voice Volume"
        )

        volume_name.setProperty(
            "class",
            "settingName",
        )

        self.volume_value = QLabel(
            "100%"
        )

        self.volume_value.setProperty(
            "class",
            "valueLabel",
        )

        volume_header.addWidget(
            volume_name
        )

        volume_header.addStretch()

        volume_header.addWidget(
            self.volume_value
        )

        voice_layout.addLayout(
            volume_header
        )

        self.volume_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.volume_slider.setRange(
            0,
            100,
        )

        self.volume_slider.setValue(
            100
        )

        self.volume_slider.valueChanged.connect(
            lambda value: self.volume_value.setText(
                f"{value}%"
            )
        )

        voice_layout.addWidget(
            self.volume_slider
        )

        content_layout.addWidget(
            voice_card
        )

        # =====================================================
        # AI
        # =====================================================

        ai_card = self._create_card()

        ai_layout = QVBoxLayout(
            ai_card
        )

        ai_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        ai_layout.setSpacing(
            10
        )

        ai_title = QLabel(
            "AI CORE"
        )

        ai_title.setProperty(
            "class",
            "sectionTitle",
        )

        ai_layout.addWidget(
            ai_title
        )

        model_row = self._setting_row(
            "AI Model",
            "Primary model used for general reasoning.",
        )

        self.model_box = QComboBox()

        self.model_box.addItems(
            [
                "gemini-3.5-flash",
                "gemini-3.5-flash-lite",
                "Automatic",
            ]
        )

        model_row.addWidget(
            self.model_box
        )

        ai_layout.addLayout(
            model_row
        )

        self.ai_enabled = QCheckBox(
            "Enable AI reasoning"
        )

        self.ai_enabled.setChecked(
            True
        )

        ai_layout.addWidget(
            self.ai_enabled
        )

        self.web_search_enabled = QCheckBox(
            "Allow web knowledge search"
        )

        self.web_search_enabled.setChecked(
            True
        )

        ai_layout.addWidget(
            self.web_search_enabled
        )

        content_layout.addWidget(
            ai_card
        )

        # =====================================================
        # HUD
        # =====================================================

        hud_card = self._create_card()

        hud_layout = QVBoxLayout(
            hud_card
        )

        hud_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        hud_layout.setSpacing(
            10
        )

        hud_title = QLabel(
            "HUD INTERFACE"
        )

        hud_title.setProperty(
            "class",
            "sectionTitle",
        )

        hud_layout.addWidget(
            hud_title
        )

        self.animations_enabled = QCheckBox(
            "Enable HUD animations"
        )

        self.animations_enabled.setChecked(
            True
        )

        hud_layout.addWidget(
            self.animations_enabled
        )

        self.pipeline_enabled = QCheckBox(
            "Show command pipeline"
        )

        self.pipeline_enabled.setChecked(
            True
        )

        hud_layout.addWidget(
            self.pipeline_enabled
        )

        self.diagnostics_enabled = QCheckBox(
            "Show system diagnostics"
        )

        self.diagnostics_enabled.setChecked(
            True
        )

        hud_layout.addWidget(
            self.diagnostics_enabled
        )

        self.transitions_enabled = QCheckBox(
            "Enable page transitions"
        )

        self.transitions_enabled.setChecked(
            True
        )

        hud_layout.addWidget(
            self.transitions_enabled
        )

        content_layout.addWidget(
            hud_card
        )

        # =====================================================
        # SYSTEM
        # =====================================================

        system_card = self._create_card()

        system_layout = QVBoxLayout(
            system_card
        )

        system_layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        system_layout.setSpacing(
            9
        )

        system_title = QLabel(
            "SYSTEM"
        )

        system_title.setProperty(
            "class",
            "sectionTitle",
        )

        system_layout.addWidget(
            system_title
        )

        system_grid = QGridLayout()

        system_grid.setHorizontalSpacing(
            24
        )

        system_grid.setVerticalSpacing(
            7
        )

        self._add_info_row(
            system_grid,
            0,
            "Application",
            "JARVIS AI 4.0",
        )

        self._add_info_row(
            system_grid,
            1,
            "Interface",
            "PySide6 HUD",
        )

        self._add_info_row(
            system_grid,
            2,
            "Automation",
            "Desktop Control",
        )

        self._add_info_row(
            system_grid,
            3,
            "Voice",
            "SpeechRecognition + SAPI5",
        )

        system_layout.addLayout(
            system_grid
        )

        content_layout.addWidget(
            system_card
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        actions = QHBoxLayout()

        actions.addStretch()

        reset_button = QPushButton(
            "RESET"
        )

        reset_button.setProperty(
            "class",
            "settingsButton",
        )

        reset_button.clicked.connect(
            self.reset_defaults
        )

        save_button = QPushButton(
            "SAVE SETTINGS"
        )

        save_button.setProperty(
            "class",
            "settingsButton",
        )

        save_button.setProperty(
            "class",
            "primaryButton",
        )

        save_button.clicked.connect(
            self.save_settings
        )

        actions.addWidget(
            reset_button
        )

        actions.addWidget(
            save_button
        )

        content_layout.addLayout(
            actions
        )

        scroll.setWidget(
            content
        )

        root.addWidget(
            scroll,
            1,
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _create_card():
        card = QFrame()

        card.setProperty(
            "class",
            "settingsCard",
        )

        return card

    @staticmethod
    def _setting_row(
        name,
        description,
    ):
        layout = QHBoxLayout()

        left = QVBoxLayout()

        name_label = QLabel(
            name
        )

        name_label.setProperty(
            "class",
            "settingName",
        )

        description_label = QLabel(
            description
        )

        description_label.setProperty(
            "class",
            "settingDescription",
        )

        left.addWidget(
            name_label
        )

        left.addWidget(
            description_label
        )

        layout.addLayout(
            left,
            1,
        )

        return layout

    @staticmethod
    def _add_info_row(
        grid,
        row,
        name,
        value,
    ):
        name_label = QLabel(
            name
        )

        name_label.setProperty(
            "class",
            "settingName",
        )

        value_label = QLabel(
            value
        )

        value_label.setProperty(
            "class",
            "valueLabel",
        )

        value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        grid.addWidget(
            name_label,
            row,
            0,
        )

        grid.addWidget(
            value_label,
            row,
            1,
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def reset_defaults(self):

        self.language_box.setCurrentText(
            "English"
        )

        self.auto_language.setChecked(
            True
        )

        self.same_language.setChecked(
            True
        )

        for language, checkbox in self.language_checks.items():
        
            checkbox.setChecked(
                True
            )
        self.wake_word_box.setCurrentIndex(
            0
        )

        self.voice_enabled.setChecked(
            True
        )

        self.rate_slider.setValue(
            175
        )

        self.volume_slider.setValue(
            100
        )

        self.model_box.setCurrentIndex(
            0
        )

        self.ai_enabled.setChecked(
            True
        )

        self.web_search_enabled.setChecked(
            True
        )

        self.animations_enabled.setChecked(
            True
        )

        self.pipeline_enabled.setChecked(
            True
        )

        self.diagnostics_enabled.setChecked(
            True
        )

        self.transitions_enabled.setChecked(
            True
        )

    def _language_changed(
        self,
        language,
    ):
        language_manager.set_primary_language(
            language
        )


    def _toggle_language(
        self,
        language,
        enabled,
    ):
        if enabled:

            language_manager.enable_language(
                language
            )

            return

        # Don't allow the current primary
        # language to be disabled.

        if (
            language
            == language_manager.get_primary_language()
        ):

            self.language_checks[
                language
            ].setChecked(
                True
            )

            return

        language_manager.disable_language(
            language
        )

    def save_settings(self):
        """Placeholder until persistent settings are implemented."""
        return

    def save_button_feedback(self):
        # Temporary visual confirmation without changing
        # the backend configuration.
        pass