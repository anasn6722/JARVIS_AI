import math

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from config.states import AssistantState
from core import app_state
from core.hud_state import hud_state
from core.system import System
from gui.widgets.diagnostics_panel import (
    DiagnosticsPanel,
)
from gui.widgets.hud_activity_panel import (
    HudActivityPanel,
)
from gui.widgets.info_card import InfoCard


class JarvisCore(QWidget):
    """Animated JARVIS core driven by the assistant state."""

    STATE_CONFIG = {
        AssistantState.SLEEPING: {
            "label": "SLEEPING",
            "color": QColor(70, 120, 130),
            "speed": 0.35,
            "pulse": 2.0,
            "glow": 0.55,
        },
        AssistantState.AWAKE: {
            "label": "AWAKE",
            "color": QColor(70, 220, 235),
            "speed": 0.9,
            "pulse": 5.0,
            "glow": 1.0,
        },
        AssistantState.LISTENING: {
            "label": "LISTENING",
            "color": QColor(90, 245, 205),
            "speed": 1.7,
            "pulse": 9.0,
            "glow": 1.2,
        },
        AssistantState.THINKING: {
            "label": "THINKING",
            "color": QColor(90, 195, 255),
            "speed": 2.5,
            "pulse": 13.0,
            "glow": 1.35,
        },
        AssistantState.SPEAKING: {
            "label": "SPEAKING",
            "color": QColor(130, 240, 255),
            "speed": 2.0,
            "pulse": 11.0,
            "glow": 1.3,
        },
    }

    def __init__(self):
        super().__init__()

        self.setMinimumSize(
            460,
            460,
        )

        self.angle = 0.0
        self.wave = 0.0

        self.current_state = (
            AssistantState.SLEEPING
        )

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._animate
        )

        self.timer.start(30)

    def set_state(self, state):
        if not isinstance(
            state,
            AssistantState,
        ):
            return

        if self.current_state == state:
            return

        self.current_state = state

        self.update()

    def _animate(self):
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

        center_x = width / 2
        center_y = height / 2

        center = (
            center_x,
            center_y,
        )

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
        ) * 0.25

        glow_strength = (
            config["glow"]
        )

        for index in range(9):

            radius = (
                base_radius
                + 70
                - index * 8
                + pulse * 0.25
            )

            alpha = int(
                max(
                    4,
                    34
                    * glow_strength
                    * (1 - index / 10),
                )
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

        self._draw_circle(
            painter,
            center,
            base_radius + 68,
            color,
            1,
            70,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 82,
            self.angle,
            70,
            color,
            2,
            220,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 82,
            self.angle + 180,
            45,
            color,
            2,
            180,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 58,
            -self.angle * 1.6,
            90,
            color,
            2,
            200,
        )

        self._draw_circle(
            painter,
            center,
            base_radius + 42,
            color,
            1,
            110,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 32,
            self.angle * 2,
            120,
            color,
            2,
            230,
        )

        core_radius = (
            base_radius
            + pulse
        )

        painter.setBrush(
            QBrush(
                QColor(
                    4,
                    25,
                    33,
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
                    230,
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

        inner_radius = (
            core_radius * 0.68
        )

        painter.setBrush(
            QBrush(
                QColor(
                    7,
                    45,
                    56,
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
                    200,
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

        energy_radius = (
            15
            + abs(
                math.sin(self.wave)
            )
            * 8
            * config["glow"]
        )

        painter.setBrush(
            QBrush(
                QColor(
                    min(
                        color.red() + 80,
                        255,
                    ),
                    min(
                        color.green() + 10,
                        255,
                    ),
                    min(
                        color.blue() + 10,
                        255,
                    ),
                    235,
                )
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            center_x - energy_radius,
            center_y - energy_radius,
            energy_radius * 2,
            energy_radius * 2,
        )

        painter.setPen(
            QColor(
                225,
                250,
                255,
            )
        )

        font = QFont(
            "Segoe UI",
            13,
        )

        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            int(center_x - 100),
            int(center_y - 7),
            200,
            25,
            Qt.AlignmentFlag.AlignCenter,
            "J A R V I S",
        )

        state_font = QFont(
            "Segoe UI",
            8,
        )

        state_font.setBold(True)

        painter.setFont(state_font)

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                230,
            )
        )

        painter.drawText(
            int(center_x - 100),
            int(center_y + 20),
            200,
            20,
            Qt.AlignmentFlag.AlignCenter,
            config["label"],
        )

        painter.end()

    @staticmethod
    def _draw_circle(
        painter,
        center,
        radius,
        color,
        width,
        alpha,
    ):
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

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawEllipse(
            center[0] - radius,
            center[1] - radius,
            radius * 2,
            radius * 2,
        )

    @staticmethod
    def _draw_arc(
        painter,
        center,
        radius,
        angle,
        span,
        color,
        width,
        alpha,
    ):
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

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            int(
                center[0] - radius
            ),
            int(
                center[1] - radius
            ),
            int(radius * 2),
            int(radius * 2),
            int(-angle * 16),
            int(-span * 16),
        )


class DashboardPage(QWidget):
    """Live JARVIS HUD dashboard."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "dashboardPage"
        )

        self.setStyleSheet(
            """
            QWidget#dashboardPage {
                background: transparent;
            }

            QLabel#dashboardTitle {
                color: #7cecff;
                font-size: 27px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#dashboardSubtitle {
                color: #4f8f9b;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#coreStatus {
                color: #73f7dc;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            18,
            24,
            18,
        )

        layout.setSpacing(8)

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "JARVIS // COMMAND CENTER"
        )

        title.setObjectName(
            "dashboardTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "NEURAL CORE // SYSTEM TELEMETRY // "
            "DESKTOP AUTOMATION"
        )

        subtitle.setObjectName(
            "dashboardSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # =====================================================
        # CORE + ACTIVITY
        # =====================================================

        center_row = QHBoxLayout()

        center_row.setSpacing(18)

        center_row.addStretch()

        core_layout = QVBoxLayout()

        self.core = JarvisCore()

        core_status = QLabel(
            "● SLEEPING"
        )

        core_status.setObjectName(
            "coreStatus"
        )

        core_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.core_status = core_status

        core_layout.addWidget(
            self.core
        )

        core_layout.addWidget(
            core_status
        )

        core_widget = QWidget()

        core_widget.setLayout(
            core_layout
        )

        center_row.addWidget(
            core_widget
        )

        # -----------------------------------------------------
        # ACTIVITY PANEL
        # -----------------------------------------------------

        self.activity_panel = (
            HudActivityPanel()
        )

        center_row.addWidget(
            self.activity_panel
        )

        # -----------------------------------------------------
        # DIAGNOSTICS PANEL
        # -----------------------------------------------------

        self.diagnostics_panel = (
            DiagnosticsPanel()
        )

        center_row.addWidget(
            self.diagnostics_panel
        )

        center_row.addStretch()

        layout.addLayout(
            center_row,
            1,
        )

        # =====================================================
        # TELEMETRY
        # =====================================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(
            12
        )

        grid.setVerticalSpacing(
            12
        )

        self.cpu_card = InfoCard(
            "CPU LOAD",
            f"{System.cpu_usage()}%",
        )

        self.ram_card = InfoCard(
            "MEMORY USAGE",
            f"{System.ram_used()} GB",
        )

        self.ai_card = InfoCard(
            "AI CORE",
            "ONLINE",
        )

        self.voice_card = InfoCard(
            "VOICE SYSTEM",
            "READY",
        )

        grid.addWidget(
            self.cpu_card,
            0,
            0,
        )

        grid.addWidget(
            self.ram_card,
            0,
            1,
        )

        grid.addWidget(
            self.ai_card,
            0,
            2,
        )

        grid.addWidget(
            self.voice_card,
            0,
            3,
        )

        layout.addLayout(
            grid
        )

        # =====================================================
        # TIMER
        # =====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_hud
        )

        self.timer.start(500)

        self.update_hud()

    # =========================================================
    # HUD UPDATE
    # =========================================================

    def update_hud(self):
        cpu = System.cpu_usage()
        ram_used = System.ram_used()
        ram_percent = System.ram_percent()

        self.cpu_card.update_value(
            f"{cpu}%",
            cpu,
        )

        self.ram_card.update_value(
            f"{ram_used} GB",
            ram_percent,
        )

        state = (
            app_state.state_machine.state
        )

        self.core.set_state(
            state
        )

        self.core_status.setText(
            f"● {state.name}"
        )

        snapshot = hud_state.snapshot()

        self.activity_panel.refresh()
        self.diagnostics_panel.refresh()

        hud_runtime_state = (
            snapshot["state"]
        )

        if hud_runtime_state == "EXECUTING":

            self.ai_card.update_value(
                "ACTIVE",
                100,
            )

        elif state in {
            AssistantState.THINKING,
            AssistantState.LISTENING,
            AssistantState.SPEAKING,
        }:

            self.ai_card.update_value(
                "ACTIVE",
                100,
            )

        else:

            self.ai_card.update_value(
                "ONLINE",
                75,
            )

        if state == AssistantState.SPEAKING:

            self.voice_card.update_value(
                "SPEAKING",
                100,
            )

        elif state == AssistantState.LISTENING:

            self.voice_card.update_value(
                "LISTENING",
                100,
            )

        else:

            self.voice_card.update_value(
                "READY",
                65,
            )