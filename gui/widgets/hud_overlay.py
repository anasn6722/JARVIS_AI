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


class HudOverlay(QWidget):
    """Subtle cinematic HUD overlay drawn above the main interface."""

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

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._animate
        )

        # Keep the overlay inexpensive.
        self.timer.start(40)

    # =========================================================
    # ANIMATION
    # =========================================================

    def _animate(self):
        self.scan_position += 1.4
        self.phase += 0.025

        if self.scan_position > self.height():
            self.scan_position = 0.0

        self.update()

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

        # =====================================================
        # SUBTLE GRID
        # =====================================================

        grid_pen = QPen(
            QColor(
                60,
                210,
                225,
                12,
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
        # SCAN LINE
        # =====================================================

        scan_y = int(
            self.scan_position
        )

        scan_gradient_height = 42

        for offset in range(
            -scan_gradient_height,
            scan_gradient_height + 1,
        ):
            y = scan_y + offset

            if y < 0 or y >= height:
                continue

            distance = abs(offset)

            alpha = max(
                0,
                25
                - int(
                    distance * 0.55
                ),
            )

            painter.setPen(
                QPen(
                    QColor(
                        65,
                        225,
                        240,
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
        # EDGE VIGNETTE
        # =====================================================

        vignette_pen = QPen(
            QColor(
                70,
                220,
                235,
                20,
            ),
            1,
        )

        painter.setPen(
            vignette_pen
        )

        margin = 12

        painter.drawRect(
            margin,
            margin,
            width - margin * 2,
            height - margin * 2,
        )

        # =====================================================
        # CORNER HUD MARKERS
        # =====================================================

        corner_color = QColor(
            90,
            235,
            245,
            90,
        )

        corner_pen = QPen(
            corner_color,
            1.5,
        )

        painter.setPen(
            corner_pen
        )

        corner = 28
        length = 12

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
        # SOFT ENERGY PULSE
        # =====================================================

        pulse = (
            math.sin(self.phase) + 1
        ) * 0.5

        alpha = int(
            4 + pulse * 8
        )

        painter.fillRect(
            0,
            0,
            width,
            2,
            QColor(
                90,
                230,
                245,
                alpha,
            ),
        )

        painter.end()