from PySide6.QtCore import QObject, Signal


class UIEventBus(QObject):
    """Thread-safe bridge between JARVIS agents and the Qt GUI."""

    navigate_requested = Signal(int)


ui_events = UIEventBus()