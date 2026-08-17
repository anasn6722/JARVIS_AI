from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect


class PageTransition:
    """Simple holographic fade transition for Qt pages."""

    def __init__(self, widget):
        self.widget = widget
        self.effect = QGraphicsOpacityEffect(
            widget
        )

        widget.setGraphicsEffect(
            self.effect
        )

        self.animation = None

    def play(
        self,
        duration=220,
    ):
        self.animation = QPropertyAnimation(
            self.effect,
            b"opacity",
            self.widget,
        )

        self.animation.setDuration(
            duration
        )

        self.animation.setStartValue(
            0.0
        )

        self.animation.setEndValue(
            1.0
        )

        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        self.animation.start()