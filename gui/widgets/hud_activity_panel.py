from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from core.hud_state import hud_state


class HudActivityPanel(QFrame):
    """Cinematic JARVIS command pipeline and live workflow monitor."""

    PIPELINE = (
        "VOICE INPUT",
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
            "hudActivityPanel"
        )

        self.setMinimumWidth(320)
        self.setMaximumWidth(380)

        self.setStyleSheet(
            """
            QFrame#hudActivityPanel {
                background-color: rgba(5, 18, 24, 238);
                border: 1px solid #175360;
                border-radius: 14px;
            }

            QLabel#activityTitle {
                color: #7cecff;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#activityState {
                color: #73f7dc;
                font-size: 17px;
                font-weight: 700;
            }

            QLabel#stageLabel {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#stageIdle {
                color: #315861;
                font-size: 9px;
                font-weight: 700;
            }

            QLabel#stageActive {
                color: #7cecff;
                font-size: 9px;
                font-weight: 700;
            }

            QLabel#stageComplete {
                color: #73f7dc;
                font-size: 9px;
                font-weight: 700;
            }

            QLabel#activityLabel {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#activityValue {
                color: #d9faff;
                font-size: 10px;
                font-weight: 600;
            }

            QLabel#eventItem {
                color: #73cbd7;
                font-size: 9px;
            }

            QProgressBar {
                background-color: #061218;
                border: 1px solid #123e48;
                border-radius: 5px;
                height: 7px;
            }

            QProgressBar::chunk {
                background-color: #26c6da;
                border-radius: 4px;
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
            "COMMAND PIPELINE"
        )

        title.setObjectName(
            "activityTitle"
        )

        self.state_label = QLabel(
            "● IDLE"
        )

        self.state_label.setObjectName(
            "activityState"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            self.state_label
        )

        layout.addLayout(
            header
        )

        # =====================================================
        # PIPELINE
        # =====================================================

        pipeline_label = QLabel(
            "EXECUTION FLOW"
        )

        pipeline_label.setObjectName(
            "activityLabel"
        )

        layout.addWidget(
            pipeline_label
        )

        self.stage_labels = {}

        for index, stage in enumerate(
            self.PIPELINE
        ):

            row = QHBoxLayout()

            row.setSpacing(
                7
            )

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

            row.addWidget(
                indicator
            )

            row.addWidget(
                name
            )

            row.addStretch()

            step_number = QLabel(
                f"{index + 1:02d}"
            )

            step_number.setObjectName(
                "stageIdle"
            )

            row.addWidget(
                step_number
            )

            layout.addLayout(
                row
            )

            self.stage_labels[
                stage
            ] = (
                indicator,
                name,
                step_number,
            )

        # =====================================================
        # DIVIDER
        # =====================================================

        divider = QFrame()

        divider.setFixedHeight(
            1
        )

        divider.setStyleSheet(
            "background:#123e48;"
        )

        layout.addWidget(
            divider
        )

        # =====================================================
        # CURRENT EVENT
        # =====================================================

        event_label = QLabel(
            "CURRENT EVENT"
        )

        event_label.setObjectName(
            "activityLabel"
        )

        self.event_value = QLabel(
            "SYSTEM_READY"
        )

        self.event_value.setObjectName(
            "activityValue"
        )

        self.event_value.setWordWrap(
            True
        )

        layout.addWidget(
            event_label
        )

        layout.addWidget(
            self.event_value
        )

        # =====================================================
        # ACTION
        # =====================================================

        action_label = QLabel(
            "ACTION"
        )

        action_label.setObjectName(
            "activityLabel"
        )

        self.action_value = QLabel(
            "—"
        )

        self.action_value.setObjectName(
            "activityValue"
        )

        self.action_value.setWordWrap(
            True
        )

        layout.addWidget(
            action_label
        )

        layout.addWidget(
            self.action_value
        )

        # =====================================================
        # TARGET
        # =====================================================

        target_label = QLabel(
            "TARGET"
        )

        target_label.setObjectName(
            "activityLabel"
        )

        self.target_value = QLabel(
            "—"
        )

        self.target_value.setObjectName(
            "activityValue"
        )

        self.target_value.setWordWrap(
            True
        )

        layout.addWidget(
            target_label
        )

        layout.addWidget(
            self.target_value
        )

        # =====================================================
        # PROGRESS
        # =====================================================

        progress_header = QHBoxLayout()

        progress_label = QLabel(
            "PROGRESS"
        )

        progress_label.setObjectName(
            "activityLabel"
        )

        self.progress_value = QLabel(
            "0%"
        )

        self.progress_value.setObjectName(
            "activityValue"
        )

        progress_header.addWidget(
            progress_label
        )

        progress_header.addStretch()

        progress_header.addWidget(
            self.progress_value
        )

        layout.addLayout(
            progress_header
        )

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
        # RECENT EVENTS
        # =====================================================

        recent_label = QLabel(
            "RECENT EVENTS"
        )

        recent_label.setObjectName(
            "activityLabel"
        )

        layout.addSpacing(
            5
        )

        layout.addWidget(
            recent_label
        )

        self.events_layout = QVBoxLayout()

        self.events_layout.setSpacing(
            3
        )

        layout.addLayout(
            self.events_layout
        )

        layout.addStretch()

        # =====================================================
        # REFRESH TIMER
        # =====================================================

        self.refresh_timer = QTimer(
            self
        )

        self.refresh_timer.timeout.connect(
            self.refresh
        )

        self.refresh_timer.start(
            120
        )

        self.refresh()

    # =========================================================
    # STAGE DETECTION
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
            f"{event} "
            f"{state} "
            f"{action}"
        )

        if any(
            keyword in combined
            for keyword in (
                "VOICE",
                "LISTEN",
            )
        ):
            return "VOICE INPUT"

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

    # =========================================================
    # PIPELINE VISUAL
    # =========================================================

    def _update_pipeline(
        self,
        snapshot,
    ):
        current_stage = (
            self._detect_stage(
                snapshot
            )
        )

        state = str(
            snapshot.get(
                "state",
                "IDLE",
            )
        ).upper()

        if state == "ERROR":
            current_index = len(
                self.PIPELINE
            ) - 1

        elif current_stage in self.PIPELINE:

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

            indicator, name, number = (
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

                number.setObjectName(
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

                number.setObjectName(
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

                number.setObjectName(
                    "stageIdle"
                )

            for widget in (
                indicator,
                name,
                number,
            ):

                widget.style().unpolish(
                    widget
                )

                widget.style().polish(
                    widget
                )

                widget.update()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        """Refresh the live pipeline from HudState."""

        snapshot = (
            hud_state.snapshot()
        )

        state = snapshot[
            "state"
        ]

        event = snapshot[
            "event"
        ]

        action = snapshot[
            "action"
        ]

        target = snapshot[
            "target"
        ]

        progress = snapshot[
            "progress"
        ]

        # -----------------------------------------------------
        # STATE
        # -----------------------------------------------------

        self.state_label.setText(
            f"● {state}"
        )

        # -----------------------------------------------------
        # EVENT
        # -----------------------------------------------------

        self.event_value.setText(
            event
            or "—"
        )

        # -----------------------------------------------------
        # ACTION
        # -----------------------------------------------------

        self.action_value.setText(
            action
            or "—"
        )

        # -----------------------------------------------------
        # TARGET
        # -----------------------------------------------------

        self.target_value.setText(
            target
            or "—"
        )

        # -----------------------------------------------------
        # PROGRESS
        # -----------------------------------------------------

        self.progress.setValue(
            progress
        )

        self.progress_value.setText(
            f"{progress}%"
        )

        # -----------------------------------------------------
        # PIPELINE
        # -----------------------------------------------------

        self._update_pipeline(
            snapshot
        )

        # -----------------------------------------------------
        # HISTORY
        # -----------------------------------------------------

        while self.events_layout.count():

            item = self.events_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        for item in snapshot[
            "history"
        ][
            :6
        ]:

            history_label = QLabel(
                f"✓ {item['event']}"
            )

            history_label.setObjectName(
                "eventItem"
            )

            history_label.setWordWrap(
                True
            )

            self.events_layout.addWidget(
                history_label
            )