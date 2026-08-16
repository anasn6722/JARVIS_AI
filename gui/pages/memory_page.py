from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ai.memory.execution.execution_memory import ExecutionMemory
from ai.memory.goal_memory import GoalMemory


class MemoryCard(QFrame):
    """Compact holographic memory statistic card."""

    def __init__(
        self,
        title,
        value,
        subtitle,
    ):
        super().__init__()

        self.setObjectName(
            "memoryCard"
        )

        self.setStyleSheet(
            """
            QFrame#memoryCard {
                background-color: rgba(5, 19, 25, 235);
                border: 1px solid #155360;
                border-radius: 12px;
            }

            QLabel#memoryCardTitle {
                color: #4f8f9b;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#memoryCardValue {
                color: #7cecff;
                font-size: 25px;
                font-weight: 700;
            }

            QLabel#memoryCardSubtitle {
                color: #396c76;
                font-size: 8px;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            12,
            14,
            12,
        )

        layout.setSpacing(
            2
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "memoryCardTitle"
        )

        self.value_label = QLabel(
            str(value)
        )

        self.value_label.setObjectName(
            "memoryCardValue"
        )

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setObjectName(
            "memoryCardSubtitle"
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addWidget(
            subtitle_label
        )

    def set_value(self, value):
        self.value_label.setText(
            str(value)
        )


class MemoryPage(QWidget):
    """Holographic JARVIS Memory Core."""

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "memoryPage"
        )

        self.goal_memory = GoalMemory()
        self.execution_memory = (
            ExecutionMemory()
        )

        self.setStyleSheet(
            """
            QWidget#memoryPage {
                background: transparent;
            }

            QLabel#memoryTitle {
                color: #7cecff;
                font-size: 27px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#memorySubtitle {
                color: #4f8f9b;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            QLabel#sectionTitle {
                color: #4f8f9b;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QFrame#memoryPanel {
                background-color: rgba(4, 16, 22, 235);
                border: 1px solid #155360;
                border-radius: 14px;
            }

            QLabel#panelTitle {
                color: #7cecff;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#panelStatus {
                color: #73f7dc;
                font-size: 9px;
                font-weight: 700;
            }

            QListWidget {
                background-color: rgba(2, 11, 15, 190);
                color: #d8fbff;
                border: 1px solid #123e48;
                border-radius: 8px;
                padding: 5px;
                font-family: Consolas;
                font-size: 10px;
                outline: none;
            }

            QListWidget::item {
                padding: 7px;
                border-bottom: 1px solid #0d2c34;
            }

            QListWidget::item:selected {
                background-color: #10343d;
                color: #8ff7ff;
            }

            QPushButton#refreshMemory {
                background-color: #07151b;
                color: #8defff;
                border: 1px solid #185461;
                border-radius: 8px;
                padding: 7px 12px;
                font-size: 9px;
                font-weight: 700;
            }

            QPushButton#refreshMemory:hover {
                background-color: #0b252d;
                border: 1px solid #35c6da;
            }
            """
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        layout.setSpacing(
            10
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        title = QLabel(
            "JARVIS // MEMORY CORE"
        )

        title.setObjectName(
            "memoryTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "PERSISTENT KNOWLEDGE // GOALS // "
            "EXECUTION HISTORY"
        )

        subtitle.setObjectName(
            "memorySubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # =====================================================
        # MEMORY TELEMETRY
        # =====================================================

        cards = QGridLayout()

        cards.setHorizontalSpacing(
            10
        )

        cards.setVerticalSpacing(
            10
        )

        self.goal_card = MemoryCard(
            "GOALS",
            0,
            "PERSISTENT OBJECTIVES",
        )

        self.completed_goal_card = MemoryCard(
            "COMPLETED",
            0,
            "FINISHED GOALS",
        )

        self.execution_card = MemoryCard(
            "EXECUTIONS",
            0,
            "RECORDED ACTIONS",
        )

        self.success_card = MemoryCard(
            "SUCCESS RATE",
            "0%",
            "EXECUTION HEALTH",
        )

        cards.addWidget(
            self.goal_card,
            0,
            0,
        )

        cards.addWidget(
            self.completed_goal_card,
            0,
            1,
        )

        cards.addWidget(
            self.execution_card,
            0,
            2,
        )

        cards.addWidget(
            self.success_card,
            0,
            3,
        )

        layout.addLayout(
            cards
        )

        # =====================================================
        # PANELS
        # =====================================================

        panels = QHBoxLayout()

        panels.setSpacing(
            12
        )

        # -----------------------------------------------------
        # GOALS
        # -----------------------------------------------------

        goals_panel = self._create_panel(
            "GOAL MEMORY"
        )

        self.goal_list = QListWidget()

        goals_panel["layout"].addWidget(
            self.goal_list
        )

        # -----------------------------------------------------
        # EXECUTIONS
        # -----------------------------------------------------

        execution_panel = self._create_panel(
            "EXECUTION MEMORY"
        )

        self.execution_list = QListWidget()

        execution_panel["layout"].addWidget(
            self.execution_list
        )

        panels.addWidget(
            goals_panel["frame"],
            1,
        )

        panels.addWidget(
            execution_panel["frame"],
            1,
        )

        layout.addLayout(
            panels,
            1,
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = QHBoxLayout()

        self.memory_status = QLabel(
            "● MEMORY SYSTEM ONLINE"
        )

        self.memory_status.setObjectName(
            "panelStatus"
        )

        refresh_button = QPushButton(
            "REFRESH MEMORY"
        )

        refresh_button.setObjectName(
            "refreshMemory"
        )

        refresh_button.clicked.connect(
            self.refresh_memory
        )

        footer.addWidget(
            self.memory_status
        )

        footer.addStretch()

        footer.addWidget(
            refresh_button
        )

        layout.addLayout(
            footer
        )

        # =====================================================
        # AUTO REFRESH
        # =====================================================

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.refresh_memory
        )

        self.timer.start(
            2000
        )

        self.refresh_memory()

    # =========================================================
    # PANEL CREATOR
    # =========================================================

    @staticmethod
    def _create_panel(title):
        frame = QFrame()

        frame.setObjectName(
            "memoryPanel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(
            8
        )

        header = QHBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "panelTitle"
        )

        status = QLabel(
            "● LIVE"
        )

        status.setObjectName(
            "panelStatus"
        )

        header.addWidget(
            title_label
        )

        header.addStretch()

        header.addWidget(
            status
        )

        layout.addLayout(
            header
        )

        return {
            "frame": frame,
            "layout": layout,
        }

    # =========================================================
    # REFRESH MEMORY
    # =========================================================

    def refresh_memory(self):
        """Reload persistent memory and update the HUD."""

        try:
            self.goal_memory.load()
            self.execution_memory.load()

            goals = self.goal_memory.all()
            executions = (
                self.execution_memory.all()
            )

            # =================================================
            # GOAL STATISTICS
            # =================================================

            active_goals = [
                goal
                for goal in goals
                if not goal.archived
            ]

            completed_goals = [
                goal
                for goal in goals
                if goal.completed
            ]

            self.goal_card.set_value(
                len(active_goals)
            )

            self.completed_goal_card.set_value(
                len(completed_goals)
            )

            # =================================================
            # EXECUTION STATISTICS
            # =================================================

            self.execution_card.set_value(
                len(executions)
            )

            successful = sum(
                1
                for execution in executions
                if execution.success
            )

            if executions:
                success_rate = (
                    successful
                    / len(executions)
                ) * 100
            else:
                success_rate = 0

            self.success_card.set_value(
                f"{success_rate:.0f}%"
            )

            # =================================================
            # GOAL LIST
            # =================================================

            self.goal_list.clear()

            if not goals:

                item = QListWidgetItem(
                    "NO PERSISTENT GOALS"
                )

                self.goal_list.addItem(
                    item
                )

            else:

                for goal in reversed(
                    goals[-20:]
                ):

                    state = getattr(
                        goal.state,
                        "value",
                        str(goal.state),
                    )

                    progress = (
                        float(
                            goal.progress
                        )
                    )

                    text = (
                        f"[{state.upper()}]  "
                        f"{goal.title}\n"
                        f"    PROGRESS: "
                        f"{progress:.0f}%"
                    )

                    item = QListWidgetItem(
                        text
                    )

                    self.goal_list.addItem(
                        item
                    )

            # =================================================
            # EXECUTION LIST
            # =================================================

            self.execution_list.clear()

            if not executions:

                item = QListWidgetItem(
                    "NO EXECUTION RECORDS"
                )

                self.execution_list.addItem(
                    item
                )

            else:

                for execution in reversed(
                    executions[-25:]
                ):

                    status = (
                        "✓"
                        if execution.success
                        else "✕"
                    )

                    action = (
                        execution.action
                    )

                    target = (
                        execution.target
                    )

                    item = QListWidgetItem(
                        f"{status} {action}\n"
                        f"    {target}"
                    )

                    self.execution_list.addItem(
                        item
                    )

            self.memory_status.setText(
                "● MEMORY SYSTEM ONLINE"
            )

        except Exception as error:

            print(
                "MemoryPage refresh error:",
                error,
            )

            self.memory_status.setText(
                "● MEMORY READ ERROR"
            )