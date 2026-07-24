from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)


class InfoCard(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setFixedSize(230, 170)

        self.setStyleSheet("""
            QFrame {
                background-color: #2B2B2B;
                border: 2px solid #3A3A3A;
                border-radius: 12px;
            }

            QLabel {
                color: white;
                border: none;
            }

            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #444444;
                text-align: center;
                color: white;
                height: 14px;
            }

            QProgressBar::chunk {
                background-color: #00D9FF;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value = QLabel(value)
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#00D9FF;
            border:none;
        """)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.setLayout(layout)

    def update_value(self, new_value, progress=None):
     """
     Update the displayed text and optionally
     set the progress bar value.
     """

     self.value.setText(str(new_value))

     if progress is None:
        try:
            number = float(
                str(new_value)
                .replace("%", "")
                .replace("GB", "")
                .strip()
            )

            progress = min(int(number), 100)

        except ValueError:
            return

     self.progress.setValue(progress)
