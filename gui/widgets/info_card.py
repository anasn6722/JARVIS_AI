from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class InfoCard(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setFixedSize(220, 140)

        self.setStyleSheet("""
            QFrame {
                background: #2B2B2B;
                border: 2px solid #3A3A3A;
                border-radius: 12px;
            }

            QLabel {
                color: white;
            }
        """)

        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value = QLabel(value)
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            color:#00D9FF;
        """)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)
        layout.addStretch()

        self.setLayout(layout)

    def update_value(self, new_value):
        """
        Update the value displayed on the card.
        """
        self.value.setText(str(new_value))