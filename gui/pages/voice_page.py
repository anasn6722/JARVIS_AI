import math
import random
from datetime import datetime

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
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from config.states import AssistantState
from core import app_state
from core.hud_state import hud_state
from voice.language_manager import language_manager


class CinematicVoiceCore(QWidget):
    """Cinematic JARVIS-inspired voice core visualization."""

    STATE_CONFIG = {
        AssistantState.SLEEPING: {
            "label": "STANDBY",
            "speed": 0.30,
            "pulse": 2.0,
            "glow": 0.45,
        },
        AssistantState.AWAKE: {
            "label": "AWAKE",
            "speed": 0.75,
            "pulse": 4.5,
            "glow": 0.85,
        },
        AssistantState.LISTENING: {
            "label": "LISTENING",
            "speed": 1.80,
            "pulse": 11.0,
            "glow": 1.35,
        },
        AssistantState.THINKING: {
            "label": "PROCESSING",
            "speed": 2.60,
            "pulse": 8.0,
            "glow": 1.10,
        },
        AssistantState.SPEAKING: {
            "label": "SPEAKING",
            "speed": 2.10,
            "pulse": 13.0,
            "glow": 1.40,
        },
    }

    def __init__(self):
        super().__init__()

        self.setMinimumSize(
            520,
            520,
        )

        self.current_state = (
            AssistantState.SLEEPING
        )

        self.angle = 0.0
        self.wave_phase = 0.0
        self.pulse_phase = 0.0

        self.audio_level = 16.0

        self.particles = []

        self._create_particles()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(30)

    # =========================================================
    # PARTICLES
    # =========================================================

    def _create_particles(self):
        self.particles.clear()

        for _ in range(70):
            angle = random.uniform(
                0,
                math.tau,
            )

            distance = random.uniform(
                140,
                265,
            )

            speed = random.uniform(
                0.0008,
                0.0020,
            )

            self.particles.append(
                {
                    "angle": angle,
                    "distance": distance,
                    "speed": speed,
                    "size": random.uniform(
                        1.0,
                        2.4,
                    ),
                    "phase": random.uniform(
                        0,
                        math.tau,
                    ),
                }
            )

    # =========================================================
    # STATE
    # =========================================================

    def set_state(self, state):
        if not isinstance(
            state,
            AssistantState,
        ):
            return

        self.current_state = state
        self.update()

    # =========================================================
    # AUDIO LEVEL
    # =========================================================

    def set_audio_level(self, level):
        self.audio_level = max(
            0.0,
            min(
                float(level),
                100.0,
            ),
        )

    # =========================================================
    # ANIMATION
    # =========================================================

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

        self.wave_phase += 0.14

        self.pulse_phase += 0.08

        if self.current_state not in {
            AssistantState.LISTENING,
            AssistantState.SPEAKING,
        }:
            self.audio_level *= 0.92
        for particle in self.particles:
            particle["angle"] += (
                particle["speed"]
                * config["speed"]
            )

        self.update()

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

        cx = width / 2
        cy = height / 2

        config = self.STATE_CONFIG.get(
            self.current_state,
            self.STATE_CONFIG[
                AssistantState.SLEEPING
            ],
        )

        # -----------------------------------------------------
        # Cinematic cyan palette
        # -----------------------------------------------------

        color = QColor(
            90,
            230,
            245,
        )

        dim_color = QColor(
            56,
            125,
            136,
        )

        bright_color = QColor(
            150,
            255,
            255,
        )

        pulse = (
            math.sin(
                self.pulse_phase
            )
            * config["pulse"]
        )

        core_radius = (
            58
            + pulse * 0.55
            + (
                self.audio_level
                * 0.055
                if self.current_state
                in {
                    AssistantState.LISTENING,
                    AssistantState.SPEAKING,
                }
                else 0
            )
        )

        # =====================================================
        # OUTER GLOW
        # =====================================================

        for index in range(12):
            radius = (
                72
                + index * 8
                + pulse * 0.12
            )

            alpha = int(
                max(
                    3,
                    25
                    * config["glow"]
                    * (
                        1
                        - index / 13
                    ),
                )
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    alpha,
                )
            )

            painter.drawEllipse(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2,
            )

        # =====================================================
        # PARTICLE FIELD
        # =====================================================

        for particle in self.particles:
            distance = particle[
                "distance"
            ]

            particle_angle = (
                particle["angle"]
                + self.angle * 0.004
            )

            px = (
                cx
                + math.cos(
                    particle_angle
                )
                * distance
            )

            py = (
                cy
                + math.sin(
                    particle_angle
                )
                * distance
            )

            twinkle = (
                0.55
                + 0.45
                * math.sin(
                    self.wave_phase
                    + particle["phase"]
                )
            )

            alpha = int(
                30
                + 85
                * twinkle
                * config["glow"]
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor(
                    bright_color.red(),
                    bright_color.green(),
                    bright_color.blue(),
                    min(
                        alpha,
                        190,
                    ),
                )
            )

            size = particle["size"]

            painter.drawEllipse(
                px - size,
                py - size,
                size * 2,
                size * 2,
            )

        # =====================================================
        # OUTER TACTICAL RINGS
        # =====================================================

        self._draw_ring(
            painter,
            cx,
            cy,
            235,
            dim_color,
            1,
            65,
        )

        self._draw_ring(
            painter,
            cx,
            cy,
            205,
            color,
            1,
            90,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            252,
            self.angle,
            70,
            color,
            2,
            190,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            252,
            self.angle + 170,
            45,
            color,
            2,
            150,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            224,
            -self.angle * 1.35,
            100,
            bright_color,
            2,
            185,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            188,
            self.angle * 1.8,
            90,
            color,
            2,
            170,
        )

        # =====================================================
        # RADIAL TICKS
        # =====================================================

        for index in range(36):
            tick_angle = (
                math.radians(
                    index * 10
                )
                + math.radians(
                    self.angle * 0.18
                )
            )

            inner = (
                198
                if index % 3
                else 194
            )

            outer = (
                204
                if index % 3
                else 214
            )

            x1 = (
                cx
                + math.cos(tick_angle)
                * inner
            )

            y1 = (
                cy
                + math.sin(tick_angle)
                * inner
            )

            x2 = (
                cx
                + math.cos(tick_angle)
                * outer
            )

            y2 = (
                cy
                + math.sin(tick_angle)
                * outer
            )

            alpha = (
                120
                if index % 3
                else 210
            )

            painter.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        alpha,
                    ),
                    1,
                )
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2),
            )

        # =====================================================
        # AUDIO WAVEFORM RING
        # =====================================================

        waveform_radius = (
            core_radius
            + 38
        )

        waveform_points = []

        for index in range(96):
            theta = (
                index
                / 96
                * math.tau
            )

            wave = math.sin(
                theta * 7
                + self.wave_phase
            )

            wave2 = math.sin(
                theta * 13
                - self.wave_phase * 1.7
            )

            amplitude = (
                4
                + self.audio_level
                * 0.11
            )

            radius = (
                waveform_radius
                + wave
                * amplitude
                * 0.55
                + wave2
                * amplitude
                * 0.25
            )

            waveform_points.append(
                (
                    cx
                    + math.cos(theta)
                    * radius,
                    cy
                    + math.sin(theta)
                    * radius,
                )
            )

        painter.setPen(
            QPen(
                QColor(
                    bright_color.red(),
                    bright_color.green(),
                    bright_color.blue(),
                    175,
                ),
                1.5,
            )
        )

        for index in range(
            len(waveform_points)
        ):
            x1, y1 = waveform_points[
                index
            ]

            x2, y2 = waveform_points[
                (
                    index + 1
                )
                % len(waveform_points)
            ]

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2),
            )

        # =====================================================
        # INNER HUD RINGS
        # =====================================================

        self._draw_ring(
            painter,
            cx,
            cy,
            145,
            color,
            1,
            125,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            160,
            self.angle * 2,
            115,
            bright_color,
            2,
            210,
        )

        self._draw_arc(
            painter,
            cx,
            cy,
            132,
            -self.angle * 2.2,
            85,
            color,
            2,
            180,
        )

        # =====================================================
        # CORE
        # =====================================================

        painter.setBrush(
            QColor(
                3,
                20,
                27,
                248,
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    240,
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

        inner_radius = (
            core_radius * 0.66
        )

        painter.setBrush(
            QColor(
                7,
                46,
                56,
                245,
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    bright_color.red(),
                    bright_color.green(),
                    bright_color.blue(),
                    190,
                ),
                1.5,
            )
        )

        painter.drawEllipse(
            cx - inner_radius,
            cy - inner_radius,
            inner_radius * 2,
            inner_radius * 2,
        )

        # =====================================================
        # ENERGY CORE
        # =====================================================

        energy_radius = (
            11
            + abs(
                math.sin(
                    self.pulse_phase * 1.4
                )
            )
            * 8
            + (
                self.audio_level
                * 0.06
            )
        )

        painter.setBrush(
            QColor(
                bright_color.red(),
                bright_color.green(),
                bright_color.blue(),
                235,
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            cx - energy_radius,
            cy - energy_radius,
            energy_radius * 2,
            energy_radius * 2,
        )

        # =====================================================
        # JARVIS TEXT
        # =====================================================

        painter.setPen(
            QColor(
                225,
                250,
                255,
                235,
            )
        )

        font = QFont(
            "Segoe UI",
            12,
        )

        font.setBold(
            True
        )

        painter.setFont(
            font
        )

        painter.drawText(
            int(cx - 100),
            int(cy - 9),
            200,
            24,
            Qt.AlignmentFlag.AlignCenter,
            "J A R V I S",
        )

        state_font = QFont(
            "Segoe UI",
            8,
        )

        state_font.setBold(
            True
        )

        painter.setFont(
            state_font
        )

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                225,
            )
        )

        painter.drawText(
            int(cx - 100),
            int(cy + 17),
            200,
            20,
            Qt.AlignmentFlag.AlignCenter,
            config["label"],
        )

        painter.end()

    # =========================================================
    # DRAW HELPERS
    # =========================================================

    @staticmethod
    def _draw_ring(
        painter,
        cx,
        cy,
        radius,
        color,
        width,
        alpha,
    ):
        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    alpha,
                ),
                width,
            )
        )

        painter.drawEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

    @staticmethod
    def _draw_arc(
        painter,
        cx,
        cy,
        radius,
        angle,
        span,
        color,
        width,
        alpha,
    ):
        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    alpha,
                ),
                width,
            )
        )

        painter.drawArc(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
            int(-angle * 16),
            int(-span * 16),
        )


class VoiceTelemetryPanel(QFrame):
    """Live voice telemetry panel."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "voiceTelemetry"
        )

        self.setStyleSheet(
            """
            QFrame#voiceTelemetry {
                background-color: rgba(4, 16, 22, 242);
                border: 1px solid #155360;
                border-radius: 14px;
            }

            QLabel#telemetryTitle {
                color: #7cecff;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#telemetrySection {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#telemetryName {
                color: #5a8c95;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#telemetryValue {
                color: #d9faff;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#telemetryActive {
                color: #73f7dc;
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

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(
            9
        )

        # =====================================================
        # TITLE
        # =====================================================

        title_row = QHBoxLayout()

        title = QLabel(
            "VOICE TELEMETRY"
        )

        title.setObjectName(
            "telemetryTitle"
        )

        self.online = QLabel(
            "● ONLINE"
        )

        self.online.setObjectName(
            "telemetryActive"
        )

        title_row.addWidget(
            title
        )

        title_row.addStretch()

        title_row.addWidget(
            self.online
        )

        layout.addLayout(
            title_row
        )

        self._separator(
            layout
        )

        # =====================================================
        # STATE
        # =====================================================

        self.state_value = self._add_row(
            layout,
            "ASSISTANT STATE",
            "STANDBY",
        )

        # =====================================================
        # MICROPHONE
        # =====================================================

        self.microphone_value = self._add_row(
            layout,
            "MICROPHONE",
            "ONLINE",
        )

        # =====================================================
        # ENGINE
        # =====================================================

        self.engine_value = self._add_row(
            layout,
            "SPEECH ENGINE",
            "SAPI5",
        )

        # =====================================================
        # LANGUAGE
        # =====================================================

        self.language_value = self._add_row(
            layout,
            "LANGUAGE",
            language_manager.get_primary_language(),
        )

        # =====================================================
        # MODE
        # =====================================================

        self.mode_value = self._add_row(
            layout,
            "LANGUAGE MODE",
            "AUTO",
        )

        # =====================================================
        # AUDIO
        # =====================================================

        audio_label = QLabel(
            "AUDIO INPUT"
        )

        audio_label.setObjectName(
            "telemetrySection"
        )

        layout.addWidget(
            audio_label
        )

        self.audio_value = QLabel(
            "12%"
        )

        self.audio_value.setObjectName(
            "telemetryValue"
        )

        layout.addWidget(
            self.audio_value
        )

        self.audio_bar = QProgressBar()

        self.audio_bar.setRange(
            0,
            100,
        )

        self.audio_bar.setValue(
            12
        )

        self.audio_bar.setTextVisible(
            False
        )

        layout.addWidget(
            self.audio_bar
        )

        # =====================================================
        # LAST COMMAND
        # =====================================================

        last_command_label = QLabel(
            "LAST COMMAND"
        )

        last_command_label.setObjectName(
            "telemetrySection"
        )

        layout.addWidget(
            last_command_label
        )

        self.last_command = QLabel(
            "—"
        )

        self.last_command.setWordWrap(
            True
        )

        self.last_command.setObjectName(
            "telemetryValue"
        )

        layout.addWidget(
            self.last_command
        )

        layout.addStretch()

    @staticmethod
    def _separator(
        layout,
    ):
        separator = QFrame()

        separator.setFixedHeight(
            1
        )

        separator.setStyleSheet(
            "background:#123e48;"
        )

        layout.addWidget(
            separator
        )

    @staticmethod
    def _add_row(
        layout,
        name,
        value,
    ):
        row = QHBoxLayout()

        name_label = QLabel(
            name
        )

        name_label.setObjectName(
            "telemetryName"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "telemetryValue"
        )

        value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        row.addWidget(
            name_label
        )

        row.addStretch()

        row.addWidget(
            value_label
        )

        layout.addLayout(
            row
        )

        return value_label

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(
        self,
        state,
        audio_level,
    ):
        self.state_value.setText(
            state.name
        )

        if state in {
            AssistantState.LISTENING,
            AssistantState.THINKING,
            AssistantState.SPEAKING,
        }:
            self.online.setText(
                "● ACTIVE"
            )

            self.microphone_value.setText(
                state.name
            )

        elif state == AssistantState.AWAKE:
            self.online.setText(
                "● AWAKE"
            )

            self.microphone_value.setText(
                "READY"
            )

        else:
            self.online.setText(
                "● STANDBY"
            )

            self.microphone_value.setText(
                "STANDBY"
            )

        self.language_value.setText(
            language_manager.get_primary_language()
        )

        self.mode_value.setText(
            "AUTO"
            if language_manager.is_auto_detect()
            else "FIXED"
        )

        self.audio_value.setText(
            f"{int(audio_level)}%"
        )

        self.audio_bar.setValue(
            int(audio_level)
        )

        snapshot = (
            hud_state.snapshot()
        )

        action = snapshot.get(
            "action",
            "",
        )

        target = snapshot.get(
            "target",
            "",
        )

        if action and target:
            self.last_command.setText(
                f"{action} → {target}"
            )
        elif action:
            self.last_command.setText(
                action
            )
        else:
            self.last_command.setText(
                "—"
            )


class VoiceEventPanel(QFrame):
    """Compact live workflow event stream."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "voiceEvents"
        )

        self.setStyleSheet(
            """
            QFrame#voiceEvents {
                background-color: rgba(4, 16, 22, 242);
                border: 1px solid #155360;
                border-radius: 14px;
            }

            QLabel#eventTitle {
                color: #7cecff;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#eventItem {
                color: #89dce7;
                font-size: 9px;
                font-family: Consolas;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            14,
            11,
            14,
            11,
        )

        layout.setSpacing(
            6
        )

        title = QLabel(
            "SYSTEM EVENTS"
        )

        title.setObjectName(
            "eventTitle"
        )

        layout.addWidget(
            title
        )

        self.events_layout = (
            QVBoxLayout()
        )

        self.events_layout.setSpacing(
            4
        )

        layout.addLayout(
            self.events_layout
        )

        self.refresh()

    def refresh(self):
        snapshot = (
            hud_state.snapshot()
        )

        while self.events_layout.count():

            item = self.events_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        history = snapshot.get(
            "history",
            [],
        )

        for item in history[:5]:
            timestamp = datetime.now().strftime(
                "%H:%M:%S"
            )

            event_text = item.get(
                "event",
                "SYSTEM",
            )

            label = QLabel(
                f"{timestamp}  ✓  {event_text}"
            )

            label.setObjectName(
                "eventItem"
            )

            self.events_layout.addWidget(
                label
            )


class VoicePage(QWidget):
    """Cinematic JARVIS voice command center."""

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

            QLabel#voiceStatus {
                color: #73f7dc;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#voiceHint {
                color: #396c76;
                font-size: 8px;
                letter-spacing: 1px;
            }
            """
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        layout.setSpacing(
            6
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
            "VOICE INPUT // NEURAL PROCESSING // "
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
        # STATUS
        # =====================================================

        self.voice_status = QLabel(
            "● STANDBY"
        )

        self.voice_status.setObjectName(
            "voiceStatus"
        )

        self.voice_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.voice_status
        )

        # =====================================================
        # CENTRAL AREA
        # =====================================================

        center = QHBoxLayout()

        center.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        center.setSpacing(
            12
        )

        center.addStretch(
            1
        )

        # -----------------------------------------------------
        # CINEMATIC CORE
        # -----------------------------------------------------

        core_container = QWidget()

        core_layout = QVBoxLayout(
            core_container
        )

        core_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        core_layout.setSpacing(
            4
        )

        self.core = (
            CinematicVoiceCore()
        )

        core_layout.addWidget(
            self.core
        )

        center.addWidget(
            core_container,
            2,
        )

        # -----------------------------------------------------
        # TELEMETRY
        # -----------------------------------------------------

        self.telemetry_panel = (
            VoiceTelemetryPanel()
        )

        center.addWidget(
            self.telemetry_panel,
            1,
        )

        center.addStretch(
            1
        )

        layout.addLayout(
            center,
            1,
        )

        # =====================================================
        # EVENTS
        # =====================================================

        self.event_panel = (
            VoiceEventPanel()
        )

        layout.addWidget(
            self.event_panel
        )

        # =====================================================
        # FOOTER
        # =====================================================

        hint = QLabel(
            'VOICE ENGINE ONLINE  //  SAY "JARVIS" '
            "TO ACTIVATE  //  F11 FOR IMMERSIVE HUD"
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
        # REFRESH
        # =====================================================

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.refresh_voice_state
        )

        self.timer.start(
            100
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

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        config = (
            CinematicVoiceCore.STATE_CONFIG.get(
                state,
                CinematicVoiceCore.STATE_CONFIG[
                    AssistantState.SLEEPING
                ],
            )
        )

        self.voice_status.setText(
            f"● {config['label']}"
        )

        # -----------------------------------------------------
        # Telemetry
        # -----------------------------------------------------

        snapshot = hud_state.snapshot()

        audio_level = snapshot.get(
            "audio_level",
            0,
        )

        self.core.set_audio_level(
            audio_level
        )

        self.telemetry_panel.refresh(
            state,
            audio_level,
        )

        # -----------------------------------------------------
        # Events
        # -----------------------------------------------------

        self.event_panel.refresh()