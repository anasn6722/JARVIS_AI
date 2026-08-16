import math

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from config.states import AssistantState
from core import app_state


class VoiceCoreVisual(QWidget):
    """Animated holographic microphone core."""

    STATE_CONFIG = {
        AssistantState.SLEEPING: {
            "label": "SLEEPING",
            "color": QColor(70, 120, 130),
            "speed": 0.35,
            "pulse": 2,
            "glow": 0.5,
        },
        AssistantState.AWAKE: {
            "label": "AWAKE",
            "color": QColor(70, 220, 235),
            "speed": 0.9,
            "pulse": 5,
            "glow": 1.0,
        },
        AssistantState.LISTENING: {
            "label": "LISTENING",
            "color": QColor(90, 245, 205),
            "speed": 2.0,
            "pulse": 12,
            "glow": 1.3,
        },
        AssistantState.THINKING: {
            "label": "PROCESSING",
            "color": QColor(90, 195, 255),
            "speed": 2.5,
            "pulse": 9,
            "glow": 1.15,
        },
        AssistantState.SPEAKING: {
            "label": "SPEAKING",
            "color": QColor(130, 240, 255),
            "speed": 2.2,
            "pulse": 14,
            "glow": 1.35,
        },
    }

    def __init__(self):
        super().__init__()

        self.setMinimumSize(
            360,
            360,
        )

        self.angle = 0.0
        self.wave = 0.0
        self.current_state = (
            AssistantState.SLEEPING
        )

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(30)

    def set_state(self, state):
        if not isinstance(
            state,
            AssistantState,
        ):
            return

        self.current_state = state
        self.update()

    def animate(self):
        config = self.STATE_CONFIG.get(
            self.current_state,
            self.STATE_CONFIG[
                AssistantState.SLEEPING
            ],
        )

        self.angle = (
            self.angle
            + config["speed"]
        ) % 360

        self.wave += 0.08

        self.update()

    def paintEvent(self, event):
        del event

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        cx = width / 2
        cy = height / 2

        config = self.STATE_CONFIG.get(
            self.current_state,
            self.STATE_CONFIG[
                AssistantState.SLEEPING
            ],
        )

        color = config["color"]

        pulse = (
            math.sin(self.wave)
            * config["pulse"]
        )

        base_radius = min(
            width,
            height,
        ) * 0.18

        # =====================================================
        # GLOW
        # =====================================================

        for index in range(8):

            radius = (
                base_radius
                + 58
                - index * 7
                + pulse * 0.2
            )

            alpha = int(
                max(
                    4,
                    34
                    * config["glow"]
                    * (1 - index / 9),
                )
            )

            painter.setBrush(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    alpha,
                )
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.drawEllipse(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2,
            )

        # =====================================================
        # OUTER RINGS
        # =====================================================

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    80,
                ),
                1,
            )
        )

        painter.drawEllipse(
            cx - base_radius - 62,
            cy - base_radius - 62,
            (base_radius + 62) * 2,
            (base_radius + 62) * 2,
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    180,
                ),
                2,
            )
        )

        painter.drawArc(
            int(cx - base_radius - 78),
            int(cy - base_radius - 78),
            int((base_radius + 78) * 2),
            int((base_radius + 78) * 2),
            int(-self.angle * 16),
            -80 * 16,
        )

        painter.drawArc(
            int(cx - base_radius - 78),
            int(cy - base_radius - 78),
            int((base_radius + 78) * 2),
            int((base_radius + 78) * 2),
            int((180 - self.angle) * 16),
            -50 * 16,
        )

        # =====================================================
        # INNER RING
        # =====================================================

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    130,
                ),
                1,
            )
        )

        painter.drawEllipse(
            cx - base_radius - 35,
            cy - base_radius - 35,
            (base_radius + 35) * 2,
            (base_radius + 35) * 2,
        )

        # =====================================================
        # CORE
        # =====================================================

        core_radius = (
            base_radius
            + pulse
        )

        painter.setBrush(
            QColor(
                4,
                25,
                33,
                245,
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    220,
                ),
                2,
            )
        )

        painter.drawEllipse(
            cx - core_radius,
            cy - core_radius,
            core_radius * 2,
            core_radius * 2,
        )

        # =====================================================
        # MICROPHONE SYMBOL
        # =====================================================

        mic_height = 70
        mic_width = 30

        painter.setPen(
            QPen(
                QColor(
                    215,
                    250,
                    255,
                    230,
                ),
                3,
            )
        )

        painter.drawRoundedRect(
            int(
                cx - mic_width / 2
            ),
            int(
                cy - mic_height / 2
            ),
            mic_width,
            mic_height,
            15,
            15,
        )

        painter.drawArc(
            int(cx - 34),
            int(cy - 20),
            68,
            65,
            0,
            -180 * 16,
        )

        painter.drawLine(
            int(cx),
            int(cy + 45),
            int(cx),
            int(cy + 62),
        )

        painter.drawLine(
            int(cx - 18),
            int(cy + 62),
            int(cx + 18),
            int(cy + 62),
        )

        # =====================================================
        # STATE
        # =====================================================

        painter.setPen(
            color
        )

        state_font = QFont(
            "Segoe UI",
            9,
        )

        state_font.setBold(True)

        painter.setFont(
            state_font
        )

        painter.drawText(
            int(cx - 100),
            int(cy + 105),
            200,
            25,
            Qt.AlignmentFlag.AlignCenter,
            config["label"],
        )

        painter.end()


class VoiceStatusPanel(QFrame):
    """Compact voice system telemetry."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "voiceStatusPanel"
        )

        self.setStyleSheet(
            """
            QFrame#voiceStatusPanel {
                background-color: rgba(4, 16, 22, 235);
                border: 1px solid #155360;
                border-radius: 14px;
            }

            QLabel#voiceTitle {
                color: #7cecff;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#voiceSection {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#voiceValue {
                color: #d8fbff;
                font-size: 15px;
                font-weight: 700;
            }

            QLabel#voiceOnline {
                color: #73f7dc;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#voiceActive {
                color: #7cecff;
                font-size: 11px;
                font-weight: 700;
            }

            QProgressBar {
                background-color: #061218;
                border: 1px solid #123e48;
                border-radius: 4px;
                height: 7px;
            }

            QProgressBar::chunk {
                background-color: #26c6da;
                border-radius: 3px;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(
            9
        )

        title_row = QHBoxLayout()

        title = QLabel(
            "VOICE CORE"
        )

        title.setObjectName(
            "voiceTitle"
        )

        self.status = QLabel(
            "● ONLINE"
        )

        self.status.setObjectName(
            "voiceOnline"
        )

        title_row.addWidget(
            title
        )

        title_row.addStretch()

        title_row.addWidget(
            self.status
        )

        layout.addLayout(
            title_row
        )

        self._separator(
            layout
        )

        # =====================================================
        # MICROPHONE
        # =====================================================

        microphone_label = QLabel(
            "MICROPHONE"
        )

        microphone_label.setObjectName(
            "voiceSection"
        )

        self.microphone_value = QLabel(
            "READY"
        )

        self.microphone_value.setObjectName(
            "voiceValue"
        )

        layout.addWidget(
            microphone_label
        )

        layout.addWidget(
            self.microphone_value
        )

        # =====================================================
        # INPUT LEVEL
        # =====================================================

        input_label = QLabel(
            "INPUT CHANNEL"
        )

        input_label.setObjectName(
            "voiceSection"
        )

        layout.addWidget(
            input_label
        )

        self.input_bar = QProgressBar()

        self.input_bar.setRange(
            0,
            100,
        )

        self.input_bar.setValue(
            20
        )

        self.input_bar.setTextVisible(
            False
        )

        layout.addWidget(
            self.input_bar
        )

        # =====================================================
        # ASSISTANT STATE
        # =====================================================

        state_label = QLabel(
            "ASSISTANT STATE"
        )

        state_label.setObjectName(
            "voiceSection"
        )

        self.state_value = QLabel(
            "SLEEPING"
        )

        self.state_value.setObjectName(
            "voiceValue"
        )

        layout.addWidget(
            state_label
        )

        layout.addWidget(
            self.state_value
        )

        # =====================================================
        # ENGINE
        # =====================================================

        engine_grid = QHBoxLayout()

        engine_name = QLabel(
            "SPEECH ENGINE"
        )

        engine_name.setObjectName(
            "voiceSection"
        )

        engine_value = QLabel(
            "SAPI5"
        )

        engine_value.setObjectName(
            "voiceOnline"
        )

        engine_grid.addWidget(
            engine_name
        )

        engine_grid.addStretch()

        engine_grid.addWidget(
            engine_value
        )

        layout.addLayout(
            engine_grid
        )

        layout.addStretch()

    @staticmethod
    def _separator(
        parent_layout,
    ):
        separator = QFrame()

        separator.setFixedHeight(
            1
        )

        separator.setStyleSheet(
            "background:#123e48;"
        )

        parent_layout.addWidget(
            separator
        )

    def refresh(
        self,
        state,
    ):
        self.state_value.setText(
            state.name
        )

        # -----------------------------------------------------
        # STATE COLOR / STATUS
        # -----------------------------------------------------

        active_states = {
            AssistantState.LISTENING,
            AssistantState.THINKING,
            AssistantState.SPEAKING,
        }

        if state in active_states:

            self.status.setText(
                "● ACTIVE"
            )

            self.status.setObjectName(
                "voiceActive"
            )

            self.microphone_value.setText(
                state.name
            )

            self.microphone_value.setObjectName(
                "voiceValue"
            )

            if state == AssistantState.LISTENING:
                self.input_bar.setValue(
                    90
                )

            elif state == AssistantState.THINKING:
                self.input_bar.setValue(
                    55
                )

            else:
                self.input_bar.setValue(
                    75
                )

        elif state == AssistantState.AWAKE:

            self.status.setText(
                "● AWAKE"
            )

            self.microphone_value.setText(
                "READY"
            )

            self.input_bar.setValue(
                30
            )

        else:

            self.status.setText(
                "● ONLINE"
            )

            self.microphone_value.setText(
                "STANDBY"
            )

            self.input_bar.setValue(
                10
            )

        for widget in (
            self.status,
        ):
            widget.style().unpolish(
                widget
            )

            widget.style().polish(
                widget
            )


class VoicePage(QWidget):
    """JARVIS Voice Command Center."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "voicePage"
        )

        self.setStyleSheet(
            """
            QWidget#voicePage {
                background: transparent;
            }

            QLabel#voicePageTitle {
                color: #7cecff;
                font-size: 27px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#voicePageSubtitle {
                color: #4f8f9b;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#voiceHint {
                color: #3f7781;
                font-size: 9px;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        layout.setSpacing(
            9
        )

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "JARVIS // VOICE CORE"
        )

        title.setObjectName(
            "voicePageTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "VOICE INPUT // SPEECH PROCESSING // "
            "AUDIO OUTPUT"
        )

        subtitle.setObjectName(
            "voicePageSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # =====================================================
        # MAIN AREA
        # =====================================================

        center = QHBoxLayout()

        center.setSpacing(
            18
        )

        center.addStretch()

        # -----------------------------------------------------
        # CORE
        # -----------------------------------------------------

        core_layout = QVBoxLayout()

        self.core = VoiceCoreVisual()

        core_status = QLabel(
            "● SLEEPING"
        )

        core_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        core_status.setStyleSheet(
            """
            color: #73f7dc;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            """
        )

        self.core_status = core_status

        core_layout.addWidget(
            self.core
        )

        core_layout.addWidget(
            self.core_status
        )

        core_widget = QWidget()

        core_widget.setLayout(
            core_layout
        )

        center.addWidget(
            core_widget
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_panel = (
            VoiceStatusPanel()
        )

        center.addWidget(
            self.status_panel
        )

        center.addStretch()

        layout.addLayout(
            center,
            1,
        )

        # =====================================================
        # FOOTER
        # =====================================================

        hint = QLabel(
            "VOICE ENGINE READY  //  "
            "SAY \"JARVIS\" TO WAKE THE ASSISTANT"
        )

        hint.setObjectName(
            "voiceHint"
        )

        hint.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            hint
        )

        # =====================================================
        # TIMER
        # =====================================================

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.refresh_voice_state
        )

        self.timer.start(
            150
        )

        self.refresh_voice_state()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_voice_state(self):
        state = (
            app_state.state_machine.state
        )

        self.core.set_state(
            state
        )

        self.core_status.setText(
            f"● {state.name}"
        )

        self.status_panel.refresh(
            state
        )