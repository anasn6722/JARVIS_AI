from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from core.hud_state import hud_state


class CommandConsole(QFrame):
    """Live JARVIS command and workflow transmission console."""

    PIPELINE = (
        "COMMAND",
        "REASONING",
        "PLANNER",
        "EXECUTION",
        "VERIFICATION",
        "RESPONSE",
    )

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "commandConsole"
        )

        self.setStyleSheet(
            """
            QFrame#commandConsole {
                background-color: rgba(3, 14, 19, 242);
                border: 1px solid #15505c;
                border-radius: 13px;
            }

            QLabel#consoleHeader {
                color: #70e8f5;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#consoleIndicator {
                color: #73f7dc;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#consoleLabel {
                color: #4d8d98;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#consoleText {
                color: #d6fbff;
                font-size: 11px;
                font-family: Consolas;
            }

            QLabel#consoleResponse {
                color: #9ff2ff;
                font-size: 11px;
                font-family: Consolas;
            }

            QLabel#consoleMeta {
                color: #4d8d98;
                font-size: 8px;
                font-family: Consolas;
            }

            QLabel#stageIdle {
                color: #315861;
                font-size: 8px;
                font-weight: 700;
            }

            QLabel#stageActive {
                color: #7cecff;
                font-size: 8px;
                font-weight: 700;
            }

            QLabel#stageComplete {
                color: #73f7dc;
                font-size: 8px;
                font-weight: 700;
            }

            QProgressBar {
                background-color: #061218;
                border: 1px solid #123e48;
                border-radius: 4px;
                height: 5px;
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
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(
            6
        )

        # =====================================================
        # HEADER
        # =====================================================

        header_row = QHBoxLayout()

        header = QLabel(
            "JARVIS // COMMAND TRANSMISSION"
        )

        header.setObjectName(
            "consoleHeader"
        )

        self.indicator = QLabel(
            "● ONLINE"
        )

        self.indicator.setObjectName(
            "consoleIndicator"
        )

        header_row.addWidget(
            header
        )

        header_row.addStretch()

        header_row.addWidget(
            self.indicator
        )

        layout.addLayout(
            header_row
        )

        # =====================================================
        # COMMAND
        # =====================================================

        command_label = QLabel(
            "COMMAND"
        )

        command_label.setObjectName(
            "consoleLabel"
        )

        layout.addWidget(
            command_label
        )

        self.command_label = QLabel(
            "> waiting for command..."
        )

        self.command_label.setObjectName(
            "consoleText"
        )

        self.command_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.command_label
        )

        # =====================================================
        # PIPELINE
        # =====================================================

        pipeline_label = QLabel(
            "WORKFLOW"
        )

        pipeline_label.setObjectName(
            "consoleLabel"
        )

        layout.addWidget(
            pipeline_label
        )

        self.stage_labels = {}

        pipeline_grid = QGridLayout()

        pipeline_grid.setHorizontalSpacing(
            8
        )

        pipeline_grid.setVerticalSpacing(
            3
        )

        for index, stage in enumerate(
            self.PIPELINE
        ):
            indicator = QLabel(
                "○"
            )

            indicator.setObjectName(
                "stageIdle"
            )

            name = QLabel(
                stage
            )

            name.setObjectName(
                "stageIdle"
            )

            pipeline_grid.addWidget(
                indicator,
                0,
                index,
            )

            pipeline_grid.addWidget(
                name,
                1,
                index,
            )

            self.stage_labels[
                stage
            ] = (
                indicator,
                name,
            )

        layout.addLayout(
            pipeline_grid
        )

        self.pipeline_progress = (
            QProgressBar()
        )

        self.pipeline_progress.setRange(
            0,
            100,
        )

        self.pipeline_progress.setValue(
            0
        )

        self.pipeline_progress.setTextVisible(
            False
        )

        layout.addWidget(
            self.pipeline_progress
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        response_label = QLabel(
            "RESPONSE"
        )

        response_label.setObjectName(
            "consoleLabel"
        )

        layout.addWidget(
            response_label
        )

        self.response_label = QLabel(
            "JARVIS: system ready."
        )

        self.response_label.setObjectName(
            "consoleResponse"
        )

        self.response_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.response_label
        )

        # =====================================================
        # META
        # =====================================================

        self.meta_label = QLabel(
            "CHANNEL: LOCAL // STATUS: READY"
        )

        self.meta_label.setObjectName(
            "consoleMeta"
        )

        layout.addWidget(
            self.meta_label
        )

        # =====================================================
        # REFRESH
        # =====================================================

        self.refresh_timer = QTimer(
            self
        )

        self.refresh_timer.timeout.connect(
            self.refresh_hud
        )

        self.refresh_timer.start(
            150
        )

        self.refresh_hud()

    # =========================================================
    # COMMAND
    # =========================================================

    def show_command(
        self,
        command,
    ):
        timestamp = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        self.command_label.setText(
            f"> {command}"
        )

        self.meta_label.setText(
            f"{timestamp} // CHANNEL: LOCAL // "
            "STATUS: PROCESSING"
        )

        self.indicator.setText(
            "● PROCESSING"
        )

        self.refresh_hud()

    # =========================================================
    # RESPONSE
    # =========================================================

    def show_response(
        self,
        response,
    ):
        timestamp = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        self.response_label.setText(
            f"JARVIS: {response}"
        )

        self.meta_label.setText(
            f"{timestamp} // CHANNEL: LOCAL // "
            "STATUS: COMPLETE"
        )

        self.indicator.setText(
            "● COMPLETE"
        )

        self.refresh_hud()

    # =========================================================
    # PROCESSING
    # =========================================================

    def show_processing(self):
        self.response_label.setText(
            "JARVIS: processing command..."
        )

        self.meta_label.setText(
            "CHANNEL: LOCAL // STATUS: THINKING"
        )

        self.indicator.setText(
            "● THINKING"
        )

        self.refresh_hud()

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(
        self,
        message,
    ):
        self.response_label.setText(
            f"JARVIS: {message}"
        )

        self.meta_label.setText(
            "CHANNEL: LOCAL // STATUS: ERROR"
        )

        self.indicator.setText(
            "● ERROR"
        )

        self.refresh_hud()

    # =========================================================
    # HUD
    # =========================================================

    @staticmethod
    def _detect_stage(
        snapshot,
    ):
        event = str(
            snapshot.get(
                "event",
                "",
            )
        ).upper()

        state = str(
            snapshot.get(
                "state",
                "",
            )
        ).upper()

        action = str(
            snapshot.get(
                "action",
                "",
            )
        ).upper()

        combined = (
            f"{event} {state} {action}"
        )

        if "COMMAND" in combined:
            return "COMMAND"

        if (
            "REASON" in combined
            or "THINK" in combined
        ):
            return "REASONING"

        if "PLAN" in combined:
            return "PLANNER"

        if (
            "EXECUT" in combined
            or action
        ):
            return "EXECUTION"

        if "VERIF" in combined:
            return "VERIFICATION"

        if (
            "RESPONSE" in combined
            or "FINISHED" in combined
        ):
            return "RESPONSE"

        return None

    def refresh_hud(self):
        snapshot = (
            hud_state.snapshot()
        )

        progress = int(
            snapshot.get(
                "progress",
                0,
            )
        )

        self.pipeline_progress.setValue(
            progress
        )

        current_stage = (
            self._detect_stage(
                snapshot
            )
        )

        if current_stage in self.PIPELINE:
            current_index = (
                self.PIPELINE.index(
                    current_stage
                )
            )
        else:
            current_index = -1

        for index, stage in enumerate(
            self.PIPELINE
        ):
            indicator, name = (
                self.stage_labels[
                    stage
                ]
            )

            if index < current_index:
                indicator.setText(
                    "✓"
                )

                indicator.setObjectName(
                    "stageComplete"
                )

                name.setObjectName(
                    "stageComplete"
                )

            elif index == current_index:
                indicator.setText(
                    "◉"
                )

                indicator.setObjectName(
                    "stageActive"
                )

                name.setObjectName(
                    "stageActive"
                )

            else:
                indicator.setText(
                    "○"
                )

                indicator.setObjectName(
                    "stageIdle"
                )

                name.setObjectName(
                    "stageIdle"
                )

            for widget in (
                indicator,
                name,
            ):
                widget.style().unpolish(
                    widget
                )

                widget.style().polish(
                    widget
                )

                widget.update() 