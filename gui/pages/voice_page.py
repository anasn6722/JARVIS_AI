import math

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from config.states import AssistantState
from core import app_state


class VoiceVisualizer(QWidget):
    """Animated microphone/radar visualization."""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(
            520,
            520,
        )

        self.angle = 0.0
        self.wave = 0.0
        self.state = (
            AssistantState.AWAKE
        )

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(30)

    # =========================================================
    # ANIMATION
    # =========================================================

    def animate(self):
        self.state = (
            app_state.state_machine.state
        )

        if self.state == AssistantState.LISTENING:
            speed = 3.0

        elif self.state == AssistantState.THINKING:
            speed = 2.0

        elif self.state == AssistantState.SPEAKING:
            speed = 2.5

        elif self.state == AssistantState.AWAKE:
            speed = 0.8

        else:
            speed = 0.3

        self.angle = (
            self.angle + speed
        ) % 360

        self.wave += 0.11

        self.update()

    # =========================================================
    # COLOR
    # =========================================================

    def state_color(self):
        if self.state == AssistantState.LISTENING:
            return QColor(
                75,
                245,
                210,
            )

        if self.state == AssistantState.THINKING:
            return QColor(
                85,
                190,
                255,
            )

        if self.state == AssistantState.SPEAKING:
            return QColor(
                125,
                235,
                255,
            )

        if self.state == AssistantState.SLEEPING:
            return QColor(
                70,
                100,
                110,
            )

        return QColor(
            70,
            210,
            230,
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):
        del event

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        center_x = width / 2
        center_y = height / 2

        color = self.state_color()

        # =====================================================
        # PULSE
        # =====================================================

        if self.state == AssistantState.LISTENING:
            pulse_amount = 24

        elif self.state == AssistantState.SPEAKING:
            pulse_amount = 18

        elif self.state == AssistantState.THINKING:
            pulse_amount = 13

        else:
            pulse_amount = 7

        pulse = (
            abs(
                math.sin(
                    self.wave
                )
            )
            * pulse_amount
        )

        base_radius = min(
            width,
            height,
        ) * 0.24

        # =====================================================
        # RADAR GLOW
        # =====================================================

        for index in range(8):

            radius = (
                base_radius
                + 65
                - index * 9
                + pulse * 0.25
            )

            alpha = max(
                5,
                32 - index * 4,
            )

            painter.setBrush(
                QBrush(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        alpha,
                    )
                )
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
            )

        # =====================================================
        # RADAR RINGS
        # =====================================================

        for index in range(4):

            radius = (
                base_radius
                + index * 24
            )

            painter.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        45 + index * 20,
                    ),
                    1,
                )
            )

            painter.setBrush(
                Qt.BrushStyle.NoBrush
            )

            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
            )

        # =====================================================
        # ROTATING RADAR ARC
        # =====================================================

        outer_radius = (
            base_radius + 78
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

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            int(
                center_x
                - outer_radius
            ),
            int(
                center_y
                - outer_radius
            ),
            int(
                outer_radius * 2
            ),
            int(
                outer_radius * 2
            ),
            int(
                -self.angle * 16
            ),
            int(
                -85 * 16
            ),
        )

        # =====================================================
        # CENTER
        # =====================================================

        core_radius = (
            base_radius
            + pulse * 0.45
        )

        painter.setBrush(
            QBrush(
                QColor(
                    4,
                    28,
                    37,
                    245,
                )
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    235,
                ),
                2,
            )
        )

        painter.drawEllipse(
            center_x - core_radius,
            center_y - core_radius,
            core_radius * 2,
            core_radius * 2,
        )

        # =====================================================
        # INNER CORE
        # =====================================================

        inner_radius = (
            core_radius * 0.62
        )

        painter.setBrush(
            QBrush(
                QColor(
                    7,
                    48,
                    58,
                    255,
                )
            )
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

        painter.drawEllipse(
            center_x - inner_radius,
            center_y - inner_radius,
            inner_radius * 2,
            inner_radius * 2,
        )

        # =====================================================
        # MICROPHONE CORE
        # =====================================================

        mic_radius = (
            17 + pulse * 0.2
        )

        painter.setBrush(
            QBrush(
                QColor(
                    min(
                        color.red() + 60,
                        255,
                    ),
                    min(
                        color.green() + 20,
                        255,
                    ),
                    min(
                        color.blue() + 10,
                        255,
                    ),
                    240,
                )
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            center_x - mic_radius,
            center_y - mic_radius,
            mic_radius * 2,
            mic_radius * 2,
        )

        # =====================================================
        # WAVEFORM RAYS
        # =====================================================

        if self.state == AssistantState.LISTENING:

            for index in range(24):

                angle = math.radians(
                    index * 15
                )

                wave = (
                    8
                    + abs(
                        math.sin(
                            self.wave
                            + index * 0.45
                        )
                    ) * 18
                )

                start_radius = (
                    base_radius
                    + 88
                )

                end_radius = (
                    start_radius
                    + wave
                )

                x1 = (
                    center_x
                    + math.cos(angle)
                    * start_radius
                )

                y1 = (
                    center_y
                    + math.sin(angle)
                    * start_radius
                )

                x2 = (
                    center_x
                    + math.cos(angle)
                    * end_radius
                )

                y2 = (
                    center_y
                    + math.sin(angle)
                    * end_radius
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

                painter.drawLine(
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2),
                )

        painter.end()


class VoicePage(QWidget):
    """JARVIS voice control and listening HUD."""

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

            QLabel#voiceTitle {
                color: #7cecff;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#voiceSubtitle {
                color: #4f8f9b;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#voiceState {
                color: #73f7dc;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 2px;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "VOICE // NEURAL INTERFACE"
        )

        title.setObjectName(
            "voiceTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "MICROPHONE INPUT • SPEECH RECOGNITION • "
            "VOICE RESPONSE"
        )

        subtitle.setObjectName(
            "voiceSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # =====================================================
        # VISUALIZER
        # =====================================================

        visualizer_row = QHBoxLayout()

        visualizer_row.addStretch()

        self.visualizer = VoiceVisualizer()

        visualizer_row.addWidget(
            self.visualizer
        )

        visualizer_row.addStretch()

        layout.addLayout(
            visualizer_row,
            1,
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.state_label = QLabel(
            "● AWAKE"
        )

        self.state_label.setObjectName(
            "voiceState"
        )

        self.state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.state_label
        )

        # =====================================================
        # STATE UPDATE
        # =====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_state
        )

        self.timer.start(100)

        self.update_state()

    # =========================================================
    # STATE
    # =========================================================

    def update_state(self):
        state = (
            app_state.state_machine.state
        )

        self.state_label.setText(
            f"● {state.name}"
        )