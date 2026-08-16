import math

from PySide6.QtCore import (
    QPointF,
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

from core.system import System
from gui.widgets.info_card import InfoCard


class JarvisCore(QWidget):
    """Animated central JARVIS HUD core."""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(
            420,
            420,
        )

        self.angle = 0
        self.pulse = 0
        self.pulse_direction = 1

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._animate
        )

        self.timer.start(30)

    # =========================================================
    # ANIMATION
    # =========================================================

    def _animate(self):
        self.angle = (
            self.angle + 1
        ) % 360

        self.pulse += (
            0.7
            * self.pulse_direction
        )

        if self.pulse >= 10:
            self.pulse_direction = -1

        elif self.pulse <= 0:
            self.pulse_direction = 1

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

        center = QPointF(
            self.width() / 2,
            self.height() / 2,
        )

        base_radius = min(
            self.width(),
            self.height(),
        ) * 0.28

        # =====================================================
        # BACKGROUND GLOW
        # =====================================================

        glow_radius = (
            base_radius
            + self.pulse
            + 34
        )

        for index in range(7):
            radius = (
                glow_radius
                - index * 8
            )

            alpha = max(
                0,
                36 - index * 5,
            )

            painter.setBrush(
                QBrush(
                    QColor(
                        0,
                        220,
                        255,
                        alpha,
                    )
                )
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.drawEllipse(
                center,
                radius,
                radius,
            )

        # =====================================================
        # OUTER RINGS
        # =====================================================

        self._draw_circle(
            painter,
            center,
            base_radius + 55,
            1,
            70,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 68,
            self.angle,
            95,
            2,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 68,
            self.angle + 180,
            55,
            2,
        )

        self._draw_circle(
            painter,
            center,
            base_radius + 38,
            1,
            100,
        )

        self._draw_arc(
            painter,
            center,
            base_radius + 38,
            -self.angle * 1.5,
            75,
            2,
        )

        self._draw_circle(
            painter,
            center,
            base_radius + 20,
            1,
            120,
        )

        # =====================================================
        # INNER CORE
        # =====================================================

        core_radius = (
            base_radius
            + self.pulse
        )

        painter.setBrush(
            QBrush(
                QColor(
                    4,
                    30,
                    38,
                    245,
                )
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    75,
                    228,
                    247,
                    220,
                ),
                2,
            )
        )

        painter.drawEllipse(
            center,
            core_radius,
            core_radius,
        )

        # =====================================================
        # CORE INNER CIRCLE
        # =====================================================

        inner_radius = (
            core_radius * 0.70
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
                    108,
                    241,
                    255,
                    200,
                ),
                2,
            )
        )

        painter.drawEllipse(
            center,
            inner_radius,
            inner_radius,
        )

        # =====================================================
        # CENTRAL ENERGY POINT
        # =====================================================

        energy_radius = (
            19
            + self.pulse * 0.55
        )

        painter.setBrush(
            QBrush(
                QColor(
                    110,
                    245,
                    255,
                    245,
                )
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            center,
            energy_radius,
            energy_radius,
        )

        # =====================================================
        # CENTER TEXT
        # =====================================================

        painter.setPen(
            QColor(
                225,
                251,
                255,
            )
        )

        font = QFont(
            "Segoe UI",
            15,
        )

        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "J A R V I S",
        )

        painter.end()

    # =========================================================
    # CIRCLE
    # =========================================================

    @staticmethod
    def _draw_circle(
        painter,
        center,
        radius,
        width,
        alpha,
    ):
        pen = QPen(
            QColor(
                55,
                208,
                229,
                alpha,
            ),
            width,
        )

        painter.setPen(pen)
        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawEllipse(
            center,
            radius,
            radius,
        )

    # =========================================================
    # ARC
    # =========================================================

    @staticmethod
    def _draw_arc(
        painter,
        center,
        radius,
        angle,
        span,
        width,
    ):
        pen = QPen(
            QColor(
                91,
                235,
                255,
                210,
            ),
            width,
        )

        painter.setPen(pen)

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        rect = (
            center.x() - radius,
            center.y() - radius,
            radius * 2,
            radius * 2,
        )

        painter.drawArc(
            int(rect[0]),
            int(rect[1]),
            int(rect[2]),
            int(rect[3]),
            int(-angle * 16),
            int(-span * 16),
        )


class DashboardPage(QWidget):
    """Main JARVIS HUD dashboard."""

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
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#dashboardSubtitle {
                color: #4f8f9b;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#coreStatus {
                color: #73f7dc;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            """
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            18,
            24,
            18,
        )

        layout.setSpacing(10)

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
            "SYSTEM TELEMETRY • AI CORE • "
            "DESKTOP CONTROL"
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
        # CORE AREA
        # =====================================================

        center_row = QHBoxLayout()

        center_row.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        center_row.addStretch()

        core_container = QVBoxLayout()

        self.core = JarvisCore()

        self.core.setMinimumSize(
            460,
            460,
        )

        core_status = QLabel(
            "● CORE ONLINE"
        )

        core_status.setObjectName(
            "coreStatus"
        )

        core_status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        core_container.addWidget(
            self.core
        )

        core_container.addWidget(
            core_status
        )

        center_widget = QWidget()

        center_widget.setLayout(
            core_container
        )

        center_row.addWidget(
            center_widget
        )

        center_row.addStretch()

        layout.addLayout(
            center_row,
            1,
        )

        # =====================================================
        # TELEMETRY CARDS
        # =====================================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

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
        # SYSTEM TIMER
        # =====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_system_info
        )

        self.timer.start(1000)

    # =========================================================
    # TELEMETRY
    # =========================================================

    def update_system_info(self):
        """Refresh CPU and RAM telemetry."""

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