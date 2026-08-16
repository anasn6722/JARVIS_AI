from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from config.states import AssistantState
from core import app_state
from core.hud_state import hud_state
from core.system import System


class DiagnosticsPanel(QFrame):
    """Compact JARVIS telemetry and diagnostics panel."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "diagnosticsPanel"
        )

        self.setMinimumWidth(
            365
        )

        self.setMinimumHeight(
            255
        )

        self.setStyleSheet(
            """
            QFrame#diagnosticsPanel {
                background-color: rgba(4, 16, 22, 235);
                border: 1px solid #155360;
                border-radius: 14px;
            }

            QLabel#diagTitle {
                color: #7cecff;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#diagSection {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1.5px;
            }

            QLabel#diagName {
                color: #6097a1;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }

            QLabel#diagValue {
                color: #d8fbff;
                font-size: 16px;
                font-weight: 700;
            }

            QLabel#diagSmallValue {
                color: #b6e9f0;
                font-size: 10px;
                font-weight: 600;
            }

            QLabel#diagOnline {
                color: #73f7dc;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#diagThinking {
                color: #7cecff;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#diagError {
                color: #ff667d;
                font-size: 11px;
                font-weight: 700;
            }

            QFrame#diagSeparator {
                background-color: #123e48;
                border: none;
            }

            QProgressBar {
                background-color: #061218;
                border: 1px solid #123e48;
                border-radius: 4px;
                height: 6px;
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
            8
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        title = QLabel(
            "SYSTEM DIAGNOSTICS"
        )

        title.setObjectName(
            "diagTitle"
        )

        self.status_value = QLabel(
            "● ONLINE"
        )

        self.status_value.setObjectName(
            "diagOnline"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            self.status_value
        )

        layout.addLayout(
            header
        )

        self._separator(
            layout
        )

        # =====================================================
        # RUNTIME
        # =====================================================

        runtime_title = QLabel(
            "RUNTIME"
        )

        runtime_title.setObjectName(
            "diagSection"
        )

        layout.addWidget(
            runtime_title
        )

        runtime_grid = QGridLayout()

        runtime_grid.setHorizontalSpacing(
            14
        )

        runtime_grid.setVerticalSpacing(
            7
        )

        self.ai_value = self._large_value(
            "ONLINE"
        )

        self.voice_value = self._large_value(
            "READY"
        )

        self.workflow_value = self._large_value(
            "IDLE"
        )

        runtime_grid.addLayout(
            self._metric_cell(
                "AI CORE",
                self.ai_value,
            ),
            0,
            0,
        )

        runtime_grid.addLayout(
            self._metric_cell(
                "VOICE",
                self.voice_value,
            ),
            0,
            1,
        )

        runtime_grid.addLayout(
            self._metric_cell(
                "WORKFLOW",
                self.workflow_value,
            ),
            0,
            2,
        )

        layout.addLayout(
            runtime_grid
        )

        self._separator(
            layout
        )

        # =====================================================
        # HARDWARE
        # =====================================================

        hardware_title = QLabel(
            "HARDWARE"
        )

        hardware_title.setObjectName(
            "diagSection"
        )

        layout.addWidget(
            hardware_title
        )

        hardware_grid = QGridLayout()

        hardware_grid.setHorizontalSpacing(
            14
        )

        hardware_grid.setVerticalSpacing(
            7
        )

        # CPU
        self.cpu_value = self._large_value(
            "0%"
        )

        self.cpu_bar = self._progress()

        hardware_grid.addLayout(
            self._metric_with_bar(
                "CPU",
                self.cpu_value,
                self.cpu_bar,
            ),
            0,
            0,
        )

        # RAM
        self.ram_value = self._large_value(
            "0%"
        )

        self.ram_bar = self._progress()

        hardware_grid.addLayout(
            self._metric_with_bar(
                "RAM",
                self.ram_value,
                self.ram_bar,
            ),
            0,
            1,
        )

        # DISK
        self.disk_value = self._large_value(
            "0%"
        )

        self.disk_bar = self._progress()

        hardware_grid.addLayout(
            self._metric_with_bar(
                "DISK",
                self.disk_value,
                self.disk_bar,
            ),
            1,
            0,
        )

        # TASKS
        self.tasks_value = self._large_value(
            "0 / 0"
        )

        self.tasks_bar = self._progress()

        hardware_grid.addLayout(
            self._metric_with_bar(
                "TASKS",
                self.tasks_value,
                self.tasks_bar,
            ),
            1,
            1,
        )

        layout.addLayout(
            hardware_grid
        )

        self._separator(
            layout
        )

        # =====================================================
        # ENVIRONMENT / ACTIVE WORKFLOW
        # =====================================================

        info_grid = QGridLayout()

        info_grid.setHorizontalSpacing(
            16
        )

        info_grid.setVerticalSpacing(
            6
        )

        # Environment
        environment_title = QLabel(
            "ENVIRONMENT"
        )

        environment_title.setObjectName(
            "diagSection"
        )

        info_grid.addWidget(
            environment_title,
            0,
            0,
        )

        # Workflow
        workflow_title = QLabel(
            "ACTIVE ACTION"
        )

        workflow_title.setObjectName(
            "diagSection"
        )

        info_grid.addWidget(
            workflow_title,
            0,
            1,
        )

        self.os_value = self._small_value(
            "Windows"
        )

        self.python_value = self._small_value(
            "Python"
        )

        self.processor_value = self._small_value(
            "Processor"
        )

        environment_layout = QVBoxLayout()

        environment_layout.setSpacing(
            3
        )

        environment_layout.addLayout(
            self._small_row(
                "OS",
                self.os_value,
            )
        )

        environment_layout.addLayout(
            self._small_row(
                "PYTHON",
                self.python_value,
            )
        )

        environment_layout.addLayout(
            self._small_row(
                "CPU",
                self.processor_value,
            )
        )

        info_grid.addLayout(
            environment_layout,
            1,
            0,
        )

        self.action_value = self._small_value(
            "—"
        )

        self.target_value = self._small_value(
            "—"
        )

        workflow_layout = QVBoxLayout()

        workflow_layout.setSpacing(
            3
        )


        workflow_layout.addLayout(
            self._small_row(
                "ACTION",
                self.action_value,
            )
        )
        
        workflow_layout.addLayout(
            self._small_row(
                "TARGET",
                self.target_value,
            )
        )

        info_grid.addLayout(
            workflow_layout,
            1,
            1,
        )

        layout.addLayout(
            info_grid
        )

        # Initial state
        self.refresh()

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _large_value(text):
        label = QLabel(
            str(text)
        )

        label.setObjectName(
            "diagValue"
        )

        label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        return label

    @staticmethod
    def _small_value(text):
        label = QLabel(
            str(text)
        )

        label.setObjectName(
            "diagSmallValue"
        )

        label.setWordWrap(
            True
        )

        return label

    @staticmethod
    def _progress():
        bar = QProgressBar()

        bar.setRange(
            0,
            100,
        )

        bar.setValue(
            0
        )

        bar.setTextVisible(
            False
        )

        return bar

    @staticmethod
    def _metric_cell(
        name,
        value,
    ):
        layout = QVBoxLayout()

        layout.setSpacing(
            2
        )

        title = QLabel(
            name
        )

        title.setObjectName(
            "diagName"
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            value
        )

        return layout

    @staticmethod
    def _metric_with_bar(
        name,
        value,
        bar,
    ):
        layout = QVBoxLayout()

        layout.setSpacing(
            3
        )

        header = QHBoxLayout()

        title = QLabel(
            name
        )

        title.setObjectName(
            "diagName"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            value
        )

        layout.addLayout(
            header
        )

        layout.addWidget(
            bar
        )

        return layout

    @staticmethod
    def _small_row(
        name,
        value,
    ):
        row = QHBoxLayout()

        row.setSpacing(
            8
        )

        label = QLabel(
            name
        )

        label.setObjectName(
            "diagName"
        )

        row.addWidget(
            label
        )

        row.addWidget(
            value,
            1,
        )

        return row

    @staticmethod
    def _separator(
        parent_layout,
    ):
        separator = QFrame()

        separator.setObjectName(
            "diagSeparator"
        )

        separator.setFixedHeight(
            1
        )

        parent_layout.addWidget(
            separator
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        """Refresh diagnostics from the live JARVIS systems."""

        cpu = System.cpu_usage()
        ram = System.ram_percent()
        disk = System.disk_percent()

        # -----------------------------------------------------
        # HARDWARE
        # -----------------------------------------------------

        self.cpu_value.setText(
            f"{cpu}%"
        )

        self.cpu_bar.setValue(
            int(cpu)
        )

        self.ram_value.setText(
            f"{ram}%"
        )

        self.ram_bar.setValue(
            int(ram)
        )

        self.disk_value.setText(
            f"{disk}%"
        )

        self.disk_bar.setValue(
            int(disk)
        )

        # -----------------------------------------------------
        # ENVIRONMENT
        # -----------------------------------------------------

        self.os_value.setText(
            System.operating_system()
        )

        self.python_value.setText(
            System.python_version()
        )

        processor = (
            System.processor()
            or "Unknown"
        )

        self.processor_value.setText(
            processor[:30]
        )

        # -----------------------------------------------------
        # ASSISTANT STATE
        # -----------------------------------------------------

        state = (
            app_state.state_machine.state
        )

        if state == AssistantState.SPEAKING:

            self.ai_value.setText(
                "SPEAKING"
            )

            self.ai_value.setObjectName(
                "diagThinking"
            )

            self.voice_value.setText(
                "SPEAKING"
            )

            self.voice_value.setObjectName(
                "diagThinking"
            )

        elif state in {
            AssistantState.THINKING,
            AssistantState.LISTENING,
        }:

            self.ai_value.setText(
                "ACTIVE"
            )

            self.ai_value.setObjectName(
                "diagThinking"
            )

            self.voice_value.setText(
                state.name
            )

            self.voice_value.setObjectName(
                "diagThinking"
            )

        elif state == AssistantState.AWAKE:

            self.ai_value.setText(
                "ONLINE"
            )

            self.ai_value.setObjectName(
                "diagOnline"
            )

            self.voice_value.setText(
                "AWAKE"
            )

            self.voice_value.setObjectName(
                "diagOnline"
            )

        else:

            self.ai_value.setText(
                "ONLINE"
            )

            self.ai_value.setObjectName(
                "diagOnline"
            )

            self.voice_value.setText(
                "READY"
            )

            self.voice_value.setObjectName(
                "diagOnline"
            )

        # -----------------------------------------------------
        # WORKFLOW
        # -----------------------------------------------------

        snapshot = (
            hud_state.snapshot()
        )

        workflow_state = (
            snapshot["state"]
        )

        self.workflow_value.setText(
            workflow_state
        )

        self.action_value.setText(
            snapshot["action"]
            or "—"
        )

        self.target_value.setText(
            snapshot["target"]
            or "—"
        )

        completed = snapshot[
            "completed"
        ]

        total = snapshot[
            "total"
        ]

        self.tasks_value.setText(
            f"{completed} / {total}"
        )

        self.tasks_bar.setValue(
            snapshot["progress"]
        )

        # -----------------------------------------------------
        # WORKFLOW COLOR
        # -----------------------------------------------------

        if workflow_state == "ERROR":

            self.workflow_value.setObjectName(
                "diagError"
            )

            self.status_value.setText(
                "● ERROR"
            )

            self.status_value.setObjectName(
                "diagError"
            )

        elif workflow_state == "EXECUTING":

            self.workflow_value.setObjectName(
                "diagThinking"
            )

            self.status_value.setText(
                "● EXECUTING"
            )

            self.status_value.setObjectName(
                "diagThinking"
            )

        else:

            self.workflow_value.setObjectName(
                "diagOnline"
            )

            self.status_value.setText(
                "● ONLINE"
            )

            self.status_value.setObjectName(
                "diagOnline"
            )

        # -----------------------------------------------------
        # REFRESH STYLES
        # -----------------------------------------------------

        for widget in (
            self.ai_value,
            self.voice_value,
            self.workflow_value,
            self.status_value,
        ):

            widget.style().unpolish(
                widget
            )

            widget.style().polish(
                widget
            )