import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from gui.boot_screen import BootScreen
from gui.theme import DARK_THEME
from gui.window import MainWindow


def main():
    app = QApplication(
        sys.argv
    )

    app.setStyleSheet(
        DARK_THEME
    )

    boot = BootScreen()

    boot.show()

    main_window = None

    def launch_main_window():
        nonlocal main_window

        main_window = MainWindow()

        main_window.show()

        boot.close()
        boot.deleteLater()

    def check_boot_complete():
        if (
            boot.progress.value()
            >= 100
        ):
            launch_main_window()
            return

        QTimer.singleShot(
            100,
            check_boot_complete,
        )

    QTimer.singleShot(
        1200,
        check_boot_complete,
    )

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()  