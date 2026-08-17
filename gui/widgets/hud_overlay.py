import math

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QWidget

from config.states import AssistantState
from core import app_state
from core.hud_state import hud_state


class HudOverlay(QWidget):
    """State-aware cinematic JARVIS HUD overlay."""

    STATE_CONFIG = {
        AssistantState.SLEEPING: {
            "speed": 0.8,
            "color": QColor(55, 125, 140),
            "scan_alpha": 14,
            "grid_alpha": 9,
        },
        AssistantState.AWAKE: {
            "speed": 1.2,
            "color": QColor(70, 220, 235),
            "scan_alpha": 20,
            "grid_alpha": 11,
        },
        AssistantState.LISTENING: {
            "speed": 2.8,
            "color": QColor(90, 245, 205),
            "scan_alpha": 34,
            "grid_alpha": 14,
        },
        AssistantState.THINKING: {
            "speed": 4.0,
            "color": QColor(90, 195, 255),
            "scan_alpha": 42,
            "grid_alpha": 15,
        },
        AssistantState.SPEAKING: {
            "speed": 3.2,
            "color": QColor(130, 240, 255),
            "scan_alpha": 38,
            "grid_alpha": 14,
        },
    }

    WORKFLOW_CONFIG = {
        "IDLE": {
            "speed_multiplier": 1.0,
            "color": QColor(55, 125, 140),
        },
        "EXECUTING": {
            "speed_multiplier": 1.8,
            "color": QColor(70, 220, 235),
        },
        "ERROR": {
            "speed_multiplier": 2.2,
            "color": QColor(255, 85, 110),
        },
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground,
            True,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        self.scan_position = 0.0
        self.phase = 0.0

        self.current_state = (
            AssistantState.SLEEPING
        )

        self.workflow_state = "IDLE"
        self.workflow_progress = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._animate
        )

        self.timer.start(40)

    # =========================================================
    # STATE
    # =========================================================

    def _read_state(self):
        assistant_state = (
            app_state.state_machine.state
        )

        hud_snapshot = (
            hud_state.snapshot()
        )

        workflow_state = str(
            hud_snapshot.get(
                "state",
                "IDLE",
            )
        ).upper()

        progress = int(
            hud_snapshot.get(
                "progress",
                0,
            )
        )

        self.current_state = (
            assistant_state
        )

        self.workflow_state = (
            workflow_state
        )

        self.workflow_progress = max(
            0,
            min(
                progress,
                100,
            ),
        )

    # =========================================================
    # ANIMATION
    # =========================================================

    def _animate(self):
        self._read_state()

        state_config = self.STATE_CONFIG.get(
            self.current_state,
            self.STATE_CONFIG[
                AssistantState.SLEEPING
            ],
        )

        workflow_config = self.WORKFLOW_CONFIG.get(
            self.workflow_state,
            self.WORKFLOW_CONFIG["IDLE"],
        )

        speed = (
            state_config["speed"]
            * workflow_config["speed_multiplier"]
        )

        self.scan_position += speed

        self.phase += (
            0.025
            * workflow_config["speed_multiplier"]
        )

        if self.scan_position > max(
            self.height(),
            1,
        ):
            self.scan_position = 0.0

        self.update()

    # =========================================================
    # COLORS
    # =========================================================

    def _active_color(self):
        workflow_config = (
            self.WORKFLOW_CONFIG.get(
                self.workflow_state,
                self.WORKFLOW_CONFIG["IDLE"],
            )
        )

        if self.workflow_state == "ERROR":
            return QColor(
                workflow_config["color"]
            )

        return QColor(
            self.STATE_CONFIG.get(
                self.current_state,
                self.STATE_CONFIG[
                    AssistantState.SLEEPING
                ],
            )["color"]
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):
        del event

        width = self.width()
        height = self.height()

        if width <= 0 or height <= 0:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        color = self._active_color()

        state_config = self.STATE_CONFIG.get(
            self.current_state,
            self.STATE_CONFIG[
                AssistantState.SLEEPING
            ],
        )

        workflow_config = self.WORKFLOW_CONFIG.get(
            self.workflow_state,
            self.WORKFLOW_CONFIG["IDLE"],
        )

        # =====================================================
        # GRID
        # =====================================================

        grid_alpha = (
            state_config["grid_alpha"]
        )

        if self.workflow_state == "EXECUTING":
            grid_alpha += 4

        grid_pen = QPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                grid_alpha,
            ),
            1,
        )

        painter.setPen(
            grid_pen
        )

        grid_size = 48

        for x in range(
            0,
            width,
            grid_size,
        ):
            painter.drawLine(
                x,
                0,
                x,
                height,
            )

        for y in range(
            0,
            height,
            grid_size,
        ):
            painter.drawLine(
                0,
                y,
                width,
                y,
            )

        # =====================================================
        # SCAN
        # =====================================================

        scan_y = int(
            self.scan_position
        )

        scan_alpha = (
            state_config["scan_alpha"]
        )

        if self.workflow_state == "EXECUTING":
            scan_alpha += 8

        if self.workflow_state == "ERROR":
            scan_alpha += 10

        scan_width = 44

        for offset in range(
            -scan_width,
            scan_width + 1,
        ):
            y = scan_y + offset

            if y < 0 or y >= height:
                continue

            distance = abs(
                offset
            )

            alpha = max(
                0,
                scan_alpha
                - int(
                    distance * 0.55
                ),
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
                0,
                y,
                width,
                y,
            )

        # =====================================================
        # PROGRESS LINE
        # =====================================================

        if (
            self.workflow_state
            == "EXECUTING"
            and self.workflow_progress > 0
        ):
            progress_width = int(
                width
                * (
                    self.workflow_progress
                    / 100
                )
            )

            painter.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        65,
                    ),
                    2,
                )
            )

            painter.drawLine(
                0,
                height - 3,
                progress_width,
                height - 3,
            )

        # =====================================================
        # CORNER MARKERS
        # =====================================================

        corner_alpha = (
            90
            if self.current_state
            != AssistantState.SLEEPING
            else 55
        )

        if self.workflow_state == "EXECUTING":
            corner_alpha += 15

        if self.workflow_state == "ERROR":
            corner_alpha = 125

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    corner_alpha,
                ),
                1.5,
            )
        )

        corner = 26
        length = 13

        # Top-left
        painter.drawLine(
            corner,
            corner,
            corner + length,
            corner,
        )
        painter.drawLine(
            corner,
            corner,
            corner,
            corner + length,
        )

        # Top-right
        painter.drawLine(
            width - corner,
            corner,
            width - corner - length,
            corner,
        )
        painter.drawLine(
            width - corner,
            corner,
            width - corner,
            corner + length,
        )

        # Bottom-left
        painter.drawLine(
            corner,
            height - corner,
            corner + length,
            height - corner,
        )
        painter.drawLine(
            corner,
            height - corner,
            corner,
            height - corner - length,
        )

        # Bottom-right
        painter.drawLine(
            width - corner,
            height - corner,
            width - corner - length,
            height - corner,
        )
        painter.drawLine(
            width - corner,
            height - corner,
            width - corner,
            height - corner - length,
        )

        # =====================================================
        # ERROR PULSE
        # =====================================================

        if self.workflow_state == "ERROR":
            pulse = (
                math.sin(self.phase * 4)
                + 1
            ) * 0.5

            alpha = int(
                3 + pulse * 12
            )

            painter.fillRect(
                0,
                0,
                width,
                height,
                QColor(
                    255,
                    45,
                    75,
                    alpha,
                ),
            )

        painter.end()