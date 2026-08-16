DARK_THEME = """
/* =========================================================
   JARVIS HUD — GLOBAL THEME
   ========================================================= */

QMainWindow {
    background-color: #05090d;
}

QWidget {
    background-color: #05090d;
    color: #d9faff;
    font-family: "Segoe UI";
    font-size: 14px;
}

/* =========================================================
   MAIN HUD CONTAINERS
   ========================================================= */

QFrame {
    background-color: transparent;
}

QLabel {
    color: #d9faff;
    background-color: transparent;
}

/* =========================================================
   HEADINGS
   ========================================================= */

QLabel[class="hudTitle"] {
    color: #7cecff;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 2px;
}

QLabel[class="hudSubtitle"] {
    color: #5c9eaa;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* =========================================================
   HUD PANELS
   ========================================================= */

QFrame[class="hudPanel"] {
    background-color: rgba(5, 18, 24, 220);
    border: 1px solid #164f5c;
    border-radius: 14px;
}

QFrame[class="hudPanel"]:hover {
    border: 1px solid #2c8797;
}

/* =========================================================
   HUD STATUS
   ========================================================= */

QLabel[class="statusOnline"] {
    color: #73f7dc;
    font-size: 13px;
    font-weight: 700;
}

QLabel[class="statusThinking"] {
    color: #7cecff;
    font-size: 13px;
    font-weight: 700;
}

QLabel[class="statusWarning"] {
    color: #ffd166;
    font-size: 13px;
    font-weight: 700;
}

QLabel[class="statusError"] {
    color: #ff667d;
    font-size: 13px;
    font-weight: 700;
}

/* =========================================================
   BUTTONS
   ========================================================= */

QPushButton {
    background-color: #07151b;
    color: #9eefff;
    border: 1px solid #185461;
    border-radius: 9px;
    padding: 9px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0b252d;
    border: 1px solid #35c6da;
    color: #dfffff;
}

QPushButton:pressed {
    background-color: #10343d;
    border: 1px solid #68e9fa;
}

QPushButton:checked {
    background-color: #10343d;
    border: 1px solid #35c6da;
    color: #8ff7ff;
}

/* =========================================================
   INPUTS
   ========================================================= */

QLineEdit {
    background-color: #071219;
    color: #dfffff;
    border: 1px solid #164b58;
    border-radius: 10px;
    padding: 10px 14px;
    selection-background-color: #176879;
}

QLineEdit:focus {
    border: 1px solid #3ed8ec;
}

/* =========================================================
   SCROLL BARS
   ========================================================= */

QScrollBar:vertical {
    background: #05090d;
    width: 8px;
    margin: 4px 0 4px 0;
}

QScrollBar::handle:vertical {
    background: #164f5c;
    min-height: 30px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #287f8f;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* =========================================================
   TOOLTIP
   ========================================================= */

QToolTip {
    background-color: #06151b;
    color: #dfffff;
    border: 1px solid #247080;
    padding: 6px;
}

/* =========================================================
   SELECTION
   ========================================================= */

QAbstractItemView {
    background-color: #071219;
    color: #dfffff;
    border: 1px solid #164f5c;
    selection-background-color: #10343d;
    selection-color: #ffffff;
}
"""