from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from core.hud_state import hud_state


class HudActivityPanel(QFrame):
    """Live JARVIS workflow activity monitor."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "hudActivityPanel"
        )

        self.setMinimumWidth(320)
        self.setMaximumWidth(370)

        self.setStyleSheet(
            """
            QFrame#hudActivityPanel {
                background-color: rgba(5, 18, 24, 235);
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
                font-size: 18px;
                font-weight: 700;
            }

            QLabel#activityLabel {
                color: #4f8f9b;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#activityValue {
                color: #d9faff;
                font-size: 11px;
                font-weight: 600;
            }

            QLabel#eventItem {
                color: #89dce7;
                font-size: 10px;
            }

            QProgressBar {
                background-color: #061218;
                border: 1px solid #123e48;
                border-radius: 5px;
                height: 8px;
            }

            QProgressBar::chunk {
                background-color: #26c6da;
                border-radius: 4px;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(8)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel(
            "LIVE SYSTEM ACTIVITY"
        )

        title.setObjectName(
            "activityTitle"
        )

        layout.addWidget(
            title
        )

        # =====================================================
        # STATE
        # =====================================================

        self.state_label = QLabel(
            "● IDLE"
        )

        self.state_label.setObjectName(
            "activityState"
        )

        layout.addWidget(
            self.state_label
        )

        # =====================================================
        # EVENT
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
            8
        )

        layout.addWidget(
            recent_label
        )

        self.events_layout = QVBoxLayout()

        self.events_layout.setSpacing(
            4
        )

        layout.addLayout(
            self.events_layout
        )

        layout.addStretch()

        self.refresh()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        """Refresh the panel from the global HUD state."""

        snapshot = hud_state.snapshot()

        state = snapshot["state"]
        event = snapshot["event"]
        action = snapshot["action"]
        target = snapshot["target"]
        progress = snapshot["progress"]

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
            event or "—"
        )

        # -----------------------------------------------------
        # ACTION
        # -----------------------------------------------------

        self.action_value.setText(
            action or "—"
        )

        # -----------------------------------------------------
        # TARGET
        # -----------------------------------------------------

        self.target_value.setText(
            target or "—"
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