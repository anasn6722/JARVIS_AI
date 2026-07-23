from gui.theme import DARK_THEME
import sys

from PySide6.QtWidgets import QApplication

from gui.window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()