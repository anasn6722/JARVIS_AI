from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)


class InfoCard(QFrame):
    """Futuristic telemetry card used by the JARVIS HUD."""

    def __init__(self, title, value):
        super().__init__()

        self.setObjectName("infoCard")
        self.setFixedSize(245, 150)

        self.setStyleSheet(
            """
            QFrame#infoCard {
                background-color: rgba(5, 20, 27, 225);
                border: 1px solid #155563;
                border-radius: 14px;
            }

            QFrame#infoCard:hover {
                border: 1px solid #31c9dc;
                background-color: rgba(7, 27, 35, 235);
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLabel#cardTitle {
                color: #5fa8b5;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#cardValue {
                color: #77edff;
                font-size: 28px;
                font-weight: 700;
            }

            QProgressBar {
                border: 1px solid #123e48;
                border-radius: 6px;
                background-color: #061218;
                height: 8px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #26c6da;
                border-radius: 5px;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        self.title = QLabel(str(title).upper())
        self.title.setObjectName("cardTitle")
        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.value = QLabel(str(value))
        self.value.setObjectName("cardValue")
        self.value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)
        layout.addSpacing(6)
        layout.addWidget(self.progress)

    def update_value(
        self,
        new_value,
        progress=None,
    ):
        """Update the displayed value and progress."""

        self.value.setText(
            str(new_value)
        )

        if progress is None:
            try:
                number = float(
                    str(new_value)
                    .replace("%", "")
                    .replace("GB", "")
                    .strip()
                )

                progress = min(
                    max(
                        int(number),
                        0,
                    ),
                    100,
                )

            except ValueError:
                return

        progress = min(
            max(
                int(progress),
                0,
            ),
            100,
        )

        self.progress.setValue(progress)