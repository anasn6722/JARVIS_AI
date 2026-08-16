from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
)
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class BootScreen(QWidget):
    """Cinematic JARVIS startup screen."""

    STEPS = (
        "INITIALIZING CORE",
        "LOADING AI ENGINE",
        "LOADING VOICE SYSTEM",
        "LOADING DESKTOP CONTROL",
        "LOADING HUD",
    )

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "JARVIS AI 4.0"
        )

        self.setFixedSize(
            900,
            560,
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.current_step = 0
        self.progress_value = 0

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #03080c;
            }

            QLabel#logo {
                color: #7cecff;
                font-family: "Segoe UI";
                font-size: 42px;
                font-weight: 700;
                letter-spacing: 8px;
            }

            QLabel#version {
                color: #4c8b96;
                font-family: Consolas;
                font-size: 11px;
                letter-spacing: 2px;
            }

            QLabel#status {
                color: #83edf7;
                font-family: Consolas;
                font-size: 13px;
                letter-spacing: 1px;
            }

            QLabel#bootInfo {
                color: #4f8994;
                font-family: Consolas;
                font-size: 10px;
            }

            QProgressBar {
                background-color: #07141a;
                border: 1px solid #17515d;
                border-radius: 5px;
                height: 9px;
            }

            QProgressBar::chunk {
                background-color: #28c6d9;
                border-radius: 4px;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            80,
            70,
            80,
            60,
        )

        layout.setSpacing(12)

        # =====================================================
        # LOGO
        # =====================================================

        logo = QLabel(
            "J A R V I S"
        )

        logo.setObjectName(
            "logo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            logo
        )

        # =====================================================
        # VERSION
        # =====================================================

        version = QLabel(
            "JUST A RATHER VERY INTELLIGENT SYSTEM  //  v4.0"
        )

        version.setObjectName(
            "version"
        )

        version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            version
        )

        layout.addSpacing(
            30
        )

        # =====================================================
        # CORE VISUAL
        # =====================================================

        self.core = BootCore()

        layout.addWidget(
            self.core,
            1,
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status = QLabel(
            "SYSTEM INITIALIZATION"
        )

        self.status.setObjectName(
            "status"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.status
        )

        # =====================================================
        # PROGRESS
        # =====================================================

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100,
        )

        self.progress.setValue(
            0
        )

        self.progress.setTextVisible(
            False
        )

        layout.addWidget(
            self.progress
        )

        # =====================================================
        # INFO
        # =====================================================

        self.info = QLabel(
            "SECURE LOCAL SESSION  //  STANDBY"
        )

        self.info.setObjectName(
            "bootInfo"
        )

        self.info.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.info
        )

    # =========================================================
    # START
    # =========================================================

    def start(self):
        """Start the boot animation."""

        self.current_step = 0
        self.progress_value = 0

        self.progress.setValue(
            0
        )

        QTimer.singleShot(
            400,
            self._next_step,
        )

    # =========================================================
    # NEXT STEP
    # =========================================================

    def _next_step(self):

        if self.current_step >= len(
            self.STEPS
        ):
            self._complete_boot()
            return

        step = self.STEPS[
            self.current_step
        ]

        self.status.setText(
            f"{step} ..."
        )

        self.info.setText(
            f"MODULE {self.current_step + 1:02d} "
            f"/ {len(self.STEPS):02d}  //  "
            "INITIALIZATION"
        )

        self.current_step += 1

        self.progress_value = int(
            (
                self.current_step
                / len(self.STEPS)
            )
            * 100
        )

        self.progress.setValue(
            self.progress_value
        )

        self.core.activate_step(
            self.current_step
        )

        QTimer.singleShot(
            450,
            self._mark_step_complete,
        )

    # =========================================================
    # MARK COMPLETE
    # =========================================================

    def _mark_step_complete(self):

        step_index = (
            self.current_step - 1
        )

        step = self.STEPS[
            step_index
        ]

        self.status.setText(
            f"{step}  ✓"
        )

        QTimer.singleShot(
            220,
            self._next_step,
        )

    # =========================================================
    # COMPLETE
    # =========================================================

    def _complete_boot(self):

        self.progress.setValue(
            100
        )

        self.status.setText(
            "SYSTEM ONLINE  ✓"
        )

        self.info.setText(
            "ALL SYSTEMS NOMINAL  //  "
            "ENTERING COMMAND CENTER"
        )

        self.core.set_complete()

    # =========================================================
    # SHOW
    # =========================================================

    def showEvent(self, event):
        super().showEvent(
            event
        )

        self.start()


class BootCore(QWidget):
    """Simple animated energy core for startup."""

    def __init__(self):
        super().__init__()

        self.angle = 0
        self.step = 0
        self.complete = False

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self._animate
        )

        self.timer.start(
            30
        )

    def _animate(self):
        self.angle = (
            self.angle + 2
        ) % 360

        self.update()

    def activate_step(
        self,
        step,
    ):
        self.step = step
        self.update()

    def set_complete(self):
        self.complete = True
        self.update()

    def paintEvent(self, event):
        del event

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        center_x = (
            self.width() / 2
        )

        center_y = (
            self.height() / 2
        )

        base_radius = 48

        if self.complete:
            color = QColor(
                95,
                240,
                215,
            )
        else:
            color = QColor(
                75,
                215,
                235,
            )

        # =====================================================
        # GLOW
        # =====================================================

        for index in range(
            7
        ):

            radius = (
                base_radius
                + 45
                - index * 7
            )

            alpha = max(
                5,
                32 - index * 4,
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
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
            )

        # =====================================================
        # RINGS
        # =====================================================

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                160,
            )
        )

        painter.drawEllipse(
            center_x - 70,
            center_y - 70,
            140,
            140,
        )

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                210,
            )
        )

        painter.drawArc(
            int(center_x - 84),
            int(center_y - 84),
            168,
            168,
            int(-self.angle * 16),
            -95 * 16,
        )

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                120,
            )
        )

        painter.drawArc(
            int(center_x - 62),
            int(center_y - 62),
            124,
            124,
            int(self.angle * 16),
            120 * 16,
        )

        # =====================================================
        # CENTER
        # =====================================================

        painter.setBrush(
            QColor(
                5,
                31,
                39,
                255,
            )
        )

        painter.setPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                220,
            )
        )

        painter.drawEllipse(
            center_x - base_radius,
            center_y - base_radius,
            base_radius * 2,
            base_radius * 2,
        )

        painter.setBrush(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                235,
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            center_x - 15,
            center_y - 15,
            30,
            30,
        )

        painter.end()