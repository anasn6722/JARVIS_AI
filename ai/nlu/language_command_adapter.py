from __future__ import annotations

import re
from typing import Optional, Tuple

from voice.language_manager import language_manager


class LanguageCommandAdapter:
    """
    Strict multilingual command normalization.

    Supported languages:
        English
        Urdu
        Roman Urdu
        Hindi
        Punjabi

    IMPORTANT:
        Only the currently selected language's command phrases
        are accepted.

    Application/entity names are shared because names such as
    Chrome, Edge, Firefox, VS Code, etc. are entities rather than
    command-language phrases.

    Example:

        Urdu:
            کروم کھولو
            -> open chrome

        Roman Urdu:
            chrome kholo
            -> open chrome

        English selected:
            open chrome
            -> open chrome

        Urdu selected:
            open chrome
            -> NOT normalized as an English command.
    """

    # =========================================================
    # SHARED APPLICATION / ENTITY ALIASES
    # =========================================================

    APP_ALIASES = {

        "chrome": (
            "chrome",
            "google chrome",
            "گوگل کروم",
            "کروم",
            "क्रोम",
            "गूगल क्रोम",
            "ਕਰੋਮ",
            "ਗੂਗਲ ਕਰੋਮ",
        ),

        "edge": (
            "edge",
            "microsoft edge",
            "مائیکروسافٹ ایج",
            "ایج",
            "माइक्रोसॉफ्ट एज",
            "एज",
            "ਮਾਈਕ੍ਰੋਸਾਫਟ ਐਜ",
            "ਐਜ",
        ),

        "firefox": (
            "firefox",
            "mozilla firefox",
            "فائر فاکس",
            "मोज़िला फ़ायरफ़ॉक्स",
            "फ़ायरफ़ॉक्स",
            "ਫਾਇਰਫਾਕਸ",
        ),

        "notepad": (
            "notepad",
            "note pad",
            "نوٹ پیڈ",
            "नोटपैड",
            "ਨੋਟਪੈਡ",
        ),

        "calculator": (
            "calculator",
            "calc",
            "کیلکولیٹر",
            "कैलकुलेटर",
            "ਕੈਲਕੂਲੇਟਰ",
        ),

        "file explorer": (
            "file explorer",
            "explorer",
            "windows explorer",
            "فائل ایکسپلورر",
            "فائل ایکسپلورر",
            "فائل ایکسپلورر کھولو",
            "फाइल एक्सप्लोरर",
            "फ़ाइल एक्सप्लोरर",
            "ਐਕਸਪਲੋਰਰ",
            "ਫਾਇਲ ਐਕਸਪਲੋਰਰ",
        ),

        "settings": (
            "settings",
            "windows settings",
            "سیٹنگز",
            "ونڈوز سیٹنگز",
            "सेटिंग्स",
            "विंडोज़ सेटिंग्स",
            "ਸੈਟਿੰਗਾਂ",
            "ਵਿੰਡੋਜ਼ ਸੈਟਿੰਗਾਂ",
        ),

        "task manager": (
            "task manager",
            "ٹاسک مینیجر",
            "टास्क मैनेजर",
            "ਟਾਸਕ ਮੈਨੇਜਰ",
        ),

        "command prompt": (
            "command prompt",
            "cmd",
            "کمانڈ پرامپٹ",
            "कमांड प्रॉम्प्ट",
            "ਕਮਾਂਡ ਪ੍ਰਾਂਪਟ",
        ),

        "powershell": (
            "powershell",
            "power shell",
            "پاور شیل",
            "पावरशेल",
            "ਪਾਵਰਸ਼ੈਲ",
        ),

        "vs code": (
            "vs code",
            "visual studio code",
            "وی ایس کوڈ",
            "وژول اسٹوڈیو کوڈ",
            "वीएस कोड",
            "विज़ुअल स्टूडियो कोड",
            "ਵੀਐਸ ਕੋਡ",
        ),
    }

    # =========================================================
    # LANGUAGE NAMES
    # =========================================================

    LANGUAGE_NAMES = {

        "english": "English",

        "urdu": "Urdu",
        "اردو": "Urdu",

        "roman urdu": "Roman Urdu",
        "romanurdu": "Roman Urdu",
        "رومن اردو": "Roman Urdu",

        "hindi": "Hindi",
        "हिंदी": "Hindi",
        "हिन्दी": "Hindi",

        "punjabi": "Punjabi",
        "پنجابی": "Punjabi",
        "ਪੰਜਾਬੀ": "Punjabi",
    }

    # =========================================================
    # STRICT LANGUAGE-SPECIFIC SWITCH PHRASES
    # =========================================================

    LANGUAGE_SWITCHES = {

        "English": {
            "switch to english": "English",
            "switch language to english": "English",
            "change language to english": "English",
            "change language to english please": "English",
            "set language to english": "English",
            "use english": "English",
            "talk in english": "English",
            "speak english": "English",

            "switch to urdu": "Urdu",
            "switch language to urdu": "Urdu",
            "change language to urdu": "Urdu",
            "set language to urdu": "Urdu",
            "use urdu": "Urdu",
            "talk in urdu": "Urdu",
            "speak urdu": "Urdu",

            "switch to roman urdu": "Roman Urdu",
            "switch language to roman urdu": "Roman Urdu",
            "change language to roman urdu": "Roman Urdu",
            "set language to roman urdu": "Roman Urdu",
            "use roman urdu": "Roman Urdu",
            "talk in roman urdu": "Roman Urdu",
            "speak roman urdu": "Roman Urdu",

            "switch to hindi": "Hindi",
            "switch language to hindi": "Hindi",
            "change language to hindi": "Hindi",
            "set language to hindi": "Hindi",
            "use hindi": "Hindi",
            "talk in hindi": "Hindi",
            "speak hindi": "Hindi",

            "switch to punjabi": "Punjabi",
            "switch language to punjabi": "Punjabi",
            "change language to punjabi": "Punjabi",
            "set language to punjabi": "Punjabi",
            "use punjabi": "Punjabi",
            "talk in punjabi": "Punjabi",
            "speak punjabi": "Punjabi",
        },

        "Urdu": {
            "زبان انگریزی کرو": "English",
            "زبان انگریزی کر دو": "English",
            "انگریزی میں بات کرو": "English",
            "انگریزی میں بولو": "English",

            "زبان اردو کرو": "Urdu",
            "زبان اردو کر دو": "Urdu",
            "اردو میں بات کرو": "Urdu",
            "اردو میں بات کریں": "Urdu",
            "اردو میں بولو": "Urdu",

            "زبان رومن اردو کرو": "Roman Urdu",
            "رومن اردو میں بات کرو": "Roman Urdu",
            "رومن اردو میں بولو": "Roman Urdu",

            "زبان ہندی کرو": "Hindi",
            "ہندی میں بات کرو": "Hindi",
            "ہندی میں بولو": "Hindi",

            "زبان پنجابی کرو": "Punjabi",
            "پنجابی میں بات کرو": "Punjabi",
            "پنجابی میں بولو": "Punjabi",
        },

        "Roman Urdu": {
            "zaban english karo": "English",
            "zaban english kar do": "English",
            "english mein baat karo": "English",
            "english mein bolo": "English",

            "zaban urdu karo": "Urdu",
            "zaban urdu kar do": "Urdu",
            "urdu mein baat karo": "Urdu",
            "urdu mein baat karein": "Urdu",
            "urdu mein bolo": "Urdu",

            "zaban roman urdu karo": "Roman Urdu",
            "roman urdu mein baat karo": "Roman Urdu",
            "roman urdu mein bolo": "Roman Urdu",

            "zaban hindi karo": "Hindi",
            "hindi mein baat karo": "Hindi",
            "hindi mein bolo": "Hindi",

            "zaban punjabi karo": "Punjabi",
            "punjabi mein baat karo": "Punjabi",
            "punjabi mein bolo": "Punjabi",
        },

        "Hindi": {
            "भाषा अंग्रेज़ी करो": "English",
            "भाषा अंग्रेजी करो": "English",
            "अंग्रेज़ी में बात करो": "English",
            "अंग्रेजी में बोलो": "English",

            "भाषा उर्दू करो": "Urdu",
            "उर्दू में बात करो": "Urdu",
            "उर्दू में बोलो": "Urdu",

            "भाषा रोमन उर्दू करो": "Roman Urdu",
            "रोमन उर्दू में बात करो": "Roman Urdu",
            "रोमन उर्दू में बोलो": "Roman Urdu",

            "भाषा हिंदी करो": "Hindi",
            "हिंदी में बात करो": "Hindi",
            "हिंदी में बोलो": "Hindi",

            "भाषा पंजाबी करो": "Punjabi",
            "पंजाबी में बात करो": "Punjabi",
            "पंजाबी में बोलो": "Punjabi",
        },

        "Punjabi": {
            "ਭਾਸ਼ਾ ਅੰਗਰੇਜ਼ੀ ਕਰੋ": "English",
            "ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ ਗੱਲ ਕਰੋ": "English",
            "ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ ਬੋਲੋ": "English",

            "ਭਾਸ਼ਾ ਉਰਦੂ ਕਰੋ": "Urdu",
            "ਉਰਦੂ ਵਿੱਚ ਗੱਲ ਕਰੋ": "Urdu",
            "ਉਰਦੂ ਵਿੱਚ ਬੋਲੋ": "Urdu",

            "ਭਾਸ਼ਾ ਰੋਮਨ ਉਰਦੂ ਕਰੋ": "Roman Urdu",
            "ਰੋਮਨ ਉਰਦੂ ਵਿੱਚ ਗੱਲ ਕਰੋ": "Roman Urdu",
            "ਰੋਮਨ ਉਰਦੂ ਵਿੱਚ ਬੋਲੋ": "Roman Urdu",

            "ਭਾਸ਼ਾ ਹਿੰਦੀ ਕਰੋ": "Hindi",
            "ਹਿੰਦੀ ਵਿੱਚ ਗੱਲ ਕਰੋ": "Hindi",
            "ਹਿੰਦੀ ਵਿੱਚ ਬੋਲੋ": "Hindi",

            "ਭਾਸ਼ਾ ਪੰਜਾਬੀ ਕਰੋ": "Punjabi",
            "ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰੋ": "Punjabi",
            "ਪੰਜਾਬੀ ਵਿੱਚ ਬੋਲੋ": "Punjabi",
        },
    }

    # =========================================================
    # LANGUAGE-SPECIFIC COMMAND PHRASES
    # =========================================================

    COMMANDS = {

        # =====================================================
        # ENGLISH
        # =====================================================

        "English": {

            "open": (
                "open",
                "launch",
                "start",
                "run",
                "please open",
                "please launch",
                "please start",
                "open up",
                "open this",
                "open the app",
                "open application",
            ),

            "close": (
                "close",
                "exit",
                "quit",
                "shut",
                "shut down",
                "please close",
                "please exit",
                "close this",
                "close it",
                "close the app",
                "close application",
            ),

            "close_last": (
                "close last",
                "close the last app",
                "close last app",
                "close previous app",
                "close the previous app",
                "close last application",
                "close previous application",
            ),

            "list_windows": (
                "list windows",
                "show windows",
                "show all windows",
                "show open windows",
                "show opened windows",
                "which windows are open",
                "what windows are open",
                "what apps are open",
                "which apps are open",
                "show open apps",
                "list open apps",
                "show running apps",
            ),

            "active_window": (
                "active window",
                "current window",
                "which window is active",
                "what window is active",
                "show active window",
                "what is the active window",
                "what is the current window",
                "which app is active",
                "what app is active",
                "show current window",
            ),

            "find_window": (
                "find window",
                "find the window",
                "locate window",
                "locate the window",
                "find application window",
                "find app window",
                "find a window",
            ),

            "focus_window": (
                "focus",
                "focus window",
                "focus the window",
                "switch to",
                "switch to window",
                "switch to the window",
                "bring up",
                "bring forward",
                "bring window forward",
                "bring the window forward",
                "bring to front",
                "bring the window to front",
                "show window",
                "show the window",
            ),

            "close_window": (
                "close window",
                "close the window",
                "close this window",
                "close that window",
            ),

            "minimize_window": (
                "minimize",
                "minimize window",
                "minimize the window",
                "minimize this window",
                "minimise",
                "minimise window",
                "minimise the window",
                "make window smaller",
            ),

            "maximize_window": (
                "maximize",
                "maximize window",
                "maximize the window",
                "maximize this window",
                "maximise",
                "maximise window",
                "maximise the window",
                "make window bigger",
                "make the window bigger",
                "full screen window",
                "make window full screen",
            ),

            "restore_window": (
                "restore",
                "restore window",
                "restore the window",
                "restore this window",
                "restore window size",
                "restore the window size",
                "return window to normal",
                "make window normal",
            ),

            "minimize_active_window": (
                "minimize active window",
                "minimize current window",
                "minimise active window",
                "minimise current window",
                "minimize the active window",
                "minimize the current window",
            ),

            "maximize_active_window": (
                "maximize active window",
                "maximize current window",
                "maximise active window",
                "maximise current window",
                "maximize the active window",
                "maximize the current window",
            ),

            "restore_active_window": (
                "restore active window",
                "restore current window",
                "restore the active window",
                "restore the current window",
                "return active window to normal",
                "return current window to normal",
            ),

            "mouse_position": (
                "mouse position",
                "where is my mouse",
                "where is the mouse",
                "where is my cursor",
                "where is the cursor",
                "show mouse position",
                "show cursor position",
                "tell me the mouse position",
                "tell me where the mouse is",
            ),

            "mouse_move": (
                "move mouse",
                "move the mouse",
                "move cursor",
                "move the cursor",
                "move mouse to",
                "move the mouse to",
                "move cursor to",
                "move the cursor to",
                "take mouse to",
                "take cursor to",
            ),

            "mouse_click": (
                "click",
                "click mouse",
                "mouse click",
                "left click",
                "left-click",
                "left click here",
                "left click there",
                "click here",
                "click there",
                "click on",
            ),

            "mouse_double_click": (
                "double click",
                "double-click",
                "double click here",
                "double click there",
                "double click on",
                "mouse double click",
                "double click mouse",
            ),

            "mouse_right_click": (
                "right click",
                "right-click",
                "right click here",
                "right click there",
                "right click on",
                "mouse right click",
            ),

            "mouse_middle_click": (
                "middle click",
                "middle-click",
                "middle click here",
                "middle click there",
                "middle click on",
                "mouse middle click",
            ),

            "mouse_scroll": (
                "scroll",
                "scroll up",
                "scroll down",
                "scroll upward",
                "scroll downward",
                "scroll up here",
                "scroll down here",
                "mouse scroll",
            ),

            "keyboard_type": (
                "type",
                "type this",
                "type text",
                "type this text",
                "write",
                "write this",
                "write this text",
                "enter this text",
                "input this",
                "type into",
            ),

            "keyboard_press": (
                "press",
                "press key",
                "press the key",
                "press this key",
                "hit key",
                "hit this key",
                "hit",
                "press button",
                "press the button",
            ),

            "keyboard_hotkey": (
                "hotkey",
                "hot key",
                "keyboard shortcut",
                "keyboard short cut",
                "shortcut",
                "press shortcut",
                "use shortcut",
                "use keyboard shortcut",
                "press keyboard shortcut",
            ),

            "ui_find": (
                "find the button",
                "find button",
                "find the control",
                "find the control",
                "find the element",
                "find element",
                "find the text",
                "find this button",
                "find this control",
                "locate the button",
                "locate the control",
                "locate the element",
            ),

            "ui_click": (
                "click the button",
                "click button",
                "click the control",
                "click the element",
                "click on the button",
                "click on the control",
                "click on the element",
            ),

            "ui_find_descriptor": (
                "find the button called",
                "find the control called",
                "find the element called",
                "find button called",
                "find control called",
                "find element called",
                "locate the button called",
                "locate the control called",
            ),

            "ui_click_descriptor": (
                "click the button called",
                "click the control called",
                "click the element called",
                "click button called",
                "click control called",
                "click element called",
            ),

            "ui_type_descriptor": (
                "type in the button",
                "type in the control",
                "type in the field",
                "type into the field",
                "type into the box",
                "enter text in the field",
                "enter text into the box",
                "write in the field",
            ),

            "ui_focus": (
                "focus this window",
                "focus this application",
                "focus this app",
                "focus this control",
                "focus the current window",
                "focus the current application",
                "focus this element",
                "focus on this window",
            ),

            "ui_click_at": (
                "click at",
                "click on coordinates",
                "click coordinates",
                "click at coordinates",
                "click position",
                "click at position",
            ),

            "ui_describe": (
                "describe this window",
                "describe the window",
                "describe this screen",
                "describe the screen",
                "describe current window",
                "what is on the screen",
                "what is in this window",
            ),

            "ui_type": (
                "type into",
                "type in",
                "write into",
                "write in",
                "enter text",
                "enter this text",
            ),

            "search_ui": (
                "search the interface",
                "search the screen",
                "search this window",
                "search in this window",
                "find in this window",
            ),

            "open_search_result": (
                "open search result",
                "open the search result",
                "open this search result",
                "open result",
            ),

            "path_exists": (
                "does this path exist",
                "check path",
                "check if path exists",
                "is this path available",
            ),

            "list_directory": (
                "list directory",
                "show directory",
                "show files",
                "show files in folder",
                "list files",
                "show folder contents",
            ),

            "file_info": (
                "file info",
                "file information",
                "file details",
                "details of file",
            ),

            "create_folder": (
                "create folder",
                "make folder",
                "new folder",
                "create a folder",
                "make a new folder",
            ),

            "create_file": (
                "create file",
                "make file",
                "new file",
                "create a file",
                "make a new file",
            ),

            "read_file": (
                "read file",
                "read this file",
                "read the file",
                "show file contents",
                "show contents of file",
            ),

            "copy": (
                "copy",
                "copy this",
                "copy the file",
                "copy the folder",
            ),

            "move": (
                "move",
                "move this",
                "move the file",
                "move the folder",
                "move it",
            ),

            "rename": (
                "rename",
                "rename this",
                "rename the file",
                "rename folder",
                "change name",
            ),

            "search_files": (
                "search files",
                "find files",
                "find file",
                "search for files",
                "search for file",
                "locate file",
                "locate files",
            ),

            "open_path": (
                "open path",
                "open this path",
                "open location",
                "open this location",
            ),

            "open_in_explorer": (
                "open in explorer",
                "show in explorer",
                "open folder in explorer",
                "show location in explorer",
            ),

            "search": (
                "search",
                "search for",
                "google",
                "find",
                "look up",
                "lookup",
                "please search",
                "can you search",
                "could you search",
            ),

            "youtube_search": (
                "youtube",
                "search youtube",
                "youtube search",
                "watch on youtube",
                "play on youtube",
                "find on youtube",
                "watch",
                "play",
            ),

            "time": (
                "time",
                "what time is it",
                "what is the time",
                "what's the time",
                "tell me the time",
                "current time",
                "time now",
            ),

            "weather": (
                "weather",
                "what is the weather",
                "how is the weather",
                "current weather",
                "weather today",
                "tell me the weather",
                "what's the weather",
            ),

            "identity": (
                "who are you",
                "what are you",
                "who is jarvis",
                "what is your name",
                "tell me who you are",
                "identify yourself",
            ),
        },

        # =====================================================
        # URDU
        # =====================================================

        "Urdu": {

            "open": (
                "کھولو",
                "کھول دو",
                "کھول دیں",
                "کھول دو نا",
                "چلاؤ",
                "چلا دو",
                "چلا دیں",
                "شروع کرو",
                "شروع کر دو",
                "شروع کریں",
                "آن کرو",
                "آن کر دو",
                "آن کریں",
            ),

            "close": (
                "بند کرو",
                "بند کر دو",
                "بند کریں",
                "بند کر دیں",
                "بند کرو اسے",
                "اسے بند کرو",
                "ختم کرو",
                "ختم کر دو",
            ),

            "close_last": (
                "آخری ایپ بند کرو",
                "آخری ایپ بند کر دو",
                "آخری ایپ بند کریں",
                "پچھلی ایپ بند کرو",
                "پچھلی ایپ بند کر دو",
                "پچھلی ایپ بند کریں",
                "آخری پروگرام بند کرو",
                "پچھلا پروگرام بند کرو",
            ),

            "list_windows": (
                "ونڈوز دکھاؤ",
                "ونڈوز دکھا دو",
                "ونڈوز دکھائیں",
                "تمام ونڈوز دکھاؤ",
                "تمام ونڈوز دکھا دو",
                "کھلی ونڈوز دکھاؤ",
                "کھلی ہوئی ونڈوز دکھاؤ",
                "کون سی ونڈوز کھلی ہیں",
                "کون سی ونڈوز اوپن ہیں",
                "کون سی ایپس کھلی ہیں",
                "کون سی ایپس چل رہی ہیں",
                "کھلی ایپس دکھاؤ",
                "چل رہی ایپس دکھاؤ",
            ),

            "active_window": (
                "ایکٹو ونڈو کون سی ہے",
                "ایکٹو ونڈو کیا ہے",
                "فعال ونڈو کون سی ہے",
                "موجودہ ونڈو کون سی ہے",
                "موجودہ ونڈو کیا ہے",
                "ابھی کون سی ونڈو کھلی ہے",
                "اس وقت کون سی ونڈو کھلی ہے",
                "ایکٹو ایپ کون سی ہے",
                "کون سی ایپ ایکٹو ہے",
            ),

            "find_window": (
                "ونڈو تلاش کرو",
                "ونڈو تلاش کر دو",
                "ونڈو تلاش کریں",
                "ونڈو ڈھونڈو",
                "ونڈو ڈھونڈ دو",
                "ونڈو کا پتہ لگاؤ",
                "ونڈو کا پتا لگاؤ",
                "ایپ کی ونڈو تلاش کرو",
            ),

            "focus_window": (
                "فوکس کرو",
                "ونڈو فوکس کرو",
                "ونڈو پر جاؤ",
                "اس ونڈو پر جاؤ",
                "ونڈو سامنے لاؤ",
                "ونڈو کو سامنے لاؤ",
                "ونڈو آگے لاؤ",
                "ونڈو کو آگے لاؤ",
                "ونڈو سامنے کرو",
                "اس ونڈو کو سامنے لاؤ",
            ),

            "close_window": (
                "ونڈو بند کرو",
                "یہ ونڈو بند کرو",
                "اس ونڈو کو بند کرو",
                "ونڈو بند کر دو",
                "یہ ونڈو بند کر دو",
            ),

            "minimize_window": (
                "ونڈو چھوٹی کرو",
                "ونڈو چھوٹی کر دو",
                "ونڈو چھوٹی کریں",
                "اس ونڈو کو چھوٹا کرو",
                "ونڈو نیچے کرو",
                "ونڈو کم کرو",
            ),

            "maximize_window": (
                "ونڈو بڑی کرو",
                "ونڈو بڑی کر دو",
                "ونڈو بڑی کریں",
                "اس ونڈو کو بڑا کرو",
                "ونڈو پوری اسکرین کرو",
                "ونڈو فل سکرین کرو",
                "ونڈو کو پوری اسکرین کرو",
            ),

            "restore_window": (
                "ونڈو واپس معمول پر لاؤ",
                "ونڈو دوبارہ معمول پر لاؤ",
                "ونڈو نارمل کرو",
                "ونڈو واپس نارمل کرو",
                "ونڈو کا سائز واپس کرو",
                "اس ونڈو کو نارمل کرو",
            ),

            "minimize_active_window": (
                "ایکٹو ونڈو چھوٹی کرو",
                "ایکٹو ونڈو چھوٹی کر دو",
                "فعال ونڈو چھوٹی کرو",
                "فعال ونڈو چھوٹی کر دو",
                "موجودہ ونڈو چھوٹی کرو",
                "موجودہ ونڈو چھوٹی کر دو",
            ),

            "maximize_active_window": (
                "ایکٹو ونڈو بڑی کرو",
                "ایکٹو ونڈو بڑی کر دو",
                "فعال ونڈو بڑی کرو",
                "فعال ونڈو بڑی کر دو",
                "موجودہ ونڈو بڑی کرو",
                "موجودہ ونڈو بڑی کر دو",
            ),

            "restore_active_window": (
                "ایکٹو ونڈو واپس معمول پر لاؤ",
                "ایکٹو ونڈو نارمل کرو",
                "فعال ونڈو واپس معمول پر لاؤ",
                "فعال ونڈو نارمل کرو",
                "موجودہ ونڈو واپس معمول پر لاؤ",
                "موجودہ ونڈو نارمل کرو",
            ),

            "mouse_position": (
                "ماؤس کی پوزیشن",
                "ماؤس کہاں ہے",
                "ماؤس کہاں موجود ہے",
                "کرسر کہاں ہے",
                "کرسر کی پوزیشن",
                "کرسر کی جگہ بتاؤ",
                "ماؤس کی جگہ بتاؤ",
                "ماؤس کی پوزیشن بتاؤ",
                "کرسر کی پوزیشن بتاؤ",
            ),

            "mouse_move": (
                "ماؤس حرکت کرو",
                "ماؤس ہلاؤ",
                "ماؤس لے جاؤ",
                "ماؤس کو لے جاؤ",
                "کرسر حرکت کرو",
                "کرسر ہلاؤ",
                "کرسر لے جاؤ",
                "کرسر کو لے جاؤ",
                "ماؤس یہاں لے جاؤ",
                "ماؤس وہاں لے جاؤ",
                "کرسر یہاں لے جاؤ",
                "کرسر وہاں لے جاؤ",
            ),

            "mouse_click": (
                "کلک کرو",
                "کلک کر دو",
                "ماؤس کلک کرو",
                "بائیں کلک کرو",
                "بائیں کلک کر دو",
                "یہاں کلک کرو",
                "وہاں کلک کرو",
                "اس پر کلک کرو",
                "ادھر کلک کرو",
                "اُدھر کلک کرو",
            ),

            "mouse_double_click": (
                "ڈبل کلک کرو",
                "ڈبل کلک کر دو",
                "ماؤس ڈبل کلک کرو",
                "یہاں ڈبل کلک کرو",
                "وہاں ڈبل کلک کرو",
                "اس پر ڈبل کلک کرو",
            ),

            "mouse_right_click": (
                "دائیں کلک کرو",
                "دائیں کلک کر دو",
                "رائٹ کلک کرو",
                "رائٹ کلک کر دو",
                "ماؤس پر دائیں کلک کرو",
                "یہاں دائیں کلک کرو",
                "وہاں دائیں کلک کرو",
            ),

            "mouse_middle_click": (
                "درمیانی کلک کرو",
                "درمیانی کلک کر دو",
                "مڈل کلک کرو",
                "مڈل کلک کر دو",
                "ماؤس پر درمیانی کلک کرو",
            ),

            "mouse_scroll": (
                "سکرول کرو",
                "سکرول کر دو",
                "اوپر سکرول کرو",
                "اوپر سکرول کر دو",
                "نیچے سکرول کرو",
                "نیچے سکرول کر دو",
                "اوپر کی طرف سکرول کرو",
                "نیچے کی طرف سکرول کرو",
                "ماؤس سکرول کرو",
            ),

            "keyboard_type": (
                "یہ لکھو",
                "یہ لکھ دو",
                "یہ ٹائپ کرو",
                "یہ ٹائپ کر دو",
                "متن لکھو",
                "متن ٹائپ کرو",
                "یہ متن داخل کرو",
                "یہ ٹیکسٹ لکھو",
                "یہ ٹیکسٹ ٹائپ کرو",
                "یہ لکھ دو",
            ),

            "keyboard_press": (
                "دباؤ",
                "دباؤ کی",
                "کی دباؤ",
                "کی دبائیں",
                "یہ کی دباؤ",
                "یہ کی دبائیں",
                "بٹن دباؤ",
                "بٹن دبائیں",
                "یہ بٹن دباؤ",
                "یہ بٹن دبائیں",
                "کی دبا دو",
            ),

            "keyboard_hotkey": (
                "کی بورڈ شارٹ کٹ",
                "کی بورڈ کا شارٹ کٹ",
                "شارٹ کٹ دباؤ",
                "شارٹ کٹ دبائیں",
                "شارٹ کٹ استعمال کرو",
                "شارٹ کٹ استعمال کریں",
                "کی بورڈ شارٹ کٹ دباؤ",
                "کی بورڈ شارٹ کٹ استعمال کرو",
            ),

            "ui_find": (
                "بٹن تلاش کرو",
                "بٹن تلاش کر دو",
                "کنٹرول تلاش کرو",
                "عنصر تلاش کرو",
                "ایلیمنٹ تلاش کرو",
                "اس بٹن کو تلاش کرو",
                "اس کنٹرول کو تلاش کرو",
                "اس عنصر کو تلاش کرو",
                "بٹن ڈھونڈو",
                "کنٹرول ڈھونڈو",
                "عنصر ڈھونڈو",
            ),

            "ui_click": (
                "بٹن پر کلک کرو",
                "بٹن کلک کرو",
                "کنٹرول پر کلک کرو",
                "عنصر پر کلک کرو",
                "ایلیمنٹ پر کلک کرو",
                "اس بٹن پر کلک کرو",
                "اس کنٹرول پر کلک کرو",
            ),

            "ui_find_descriptor": (
                "یہ نام والا بٹن تلاش کرو",
                "یہ نام کا بٹن تلاش کرو",
                "اس نام والا بٹن تلاش کرو",
                "اس نام کا بٹن تلاش کرو",
                "بٹن تلاش کرو جس کا نام ہے",
                "یہ نام والا کنٹرول تلاش کرو",
                "اس نام والا کنٹرول تلاش کرو",
                "اس نام کا کنٹرول تلاش کرو",
                "یہ نام والا عنصر تلاش کرو",
                "اس نام والا عنصر تلاش کرو",
                "اس نام کا عنصر تلاش کرو",
            ),

            "ui_click_descriptor": (
                "یہ نام والے بٹن پر کلک کرو",
                "اس نام والے بٹن پر کلک کرو",
                "اس نام کا بٹن کلک کرو",
                "اس نام والے کنٹرول پر کلک کرو",
                "اس نام کا کنٹرول کلک کرو",
                "اس نام والے عنصر پر کلک کرو",
                "اس نام کا عنصر کلک کرو",
            ),

            "ui_type_descriptor": (
                "فیلڈ میں لکھو",
                "فیلڈ میں یہ لکھو",
                "باکس میں لکھو",
                "باکس میں یہ لکھو",
                "فیلڈ میں ٹیکسٹ لکھو",
                "باکس میں ٹیکسٹ داخل کرو",
                "اس فیلڈ میں لکھو",
            ),

            "ui_focus": (
                "ونڈو پر فوکس کرو",
                "ونڈو کو فوکس کرو",
                "ایپلیکیشن پر فوکس کرو",
                "ایپ پر فوکس کرو",
                "کنٹرول پر فوکس کرو",
                "اس ونڈو پر فوکس کرو",
                "اس ایپ پر فوکس کرو",
            ),

            "ui_click_at": (
                "یہاں کلک کرو",
                "اس جگہ کلک کرو",
                "کوآرڈینیٹ پر کلک کرو",
                "اس کوآرڈینیٹ پر کلک کرو",
                "مقام پر کلک کرو",
                "پوزیشن پر کلک کرو",
            ),

            "ui_describe": (
                "اس ونڈو کی تفصیل بتاؤ",
                "ونڈو کی تفصیل بتاؤ",
                "اس اسکرین کی تفصیل بتاؤ",
                "اسکرین کی تفصیل بتاؤ",
                "موجودہ ونڈو کی تفصیل بتاؤ",
                "اسکرین پر کیا ہے",
                "اس ونڈو میں کیا ہے",
            ),

            "ui_type": (
                "یہاں لکھو",
                "یہاں ٹائپ کرو",
                "فیلڈ میں لکھو",
                "باکس میں لکھو",
                "یہ ٹیکسٹ لکھو",
                "یہ ٹیکسٹ داخل کرو",
            ),

            "search_ui": (
                "اسکرین میں تلاش کرو",
                "اس ونڈو میں تلاش کرو",
                "انٹرفیس میں تلاش کرو",
                "اسکرین پر تلاش کرو",
                "اس ونڈو میں ڈھونڈو",
            ),

            "open_search_result": (
                "تلاش کا نتیجہ کھولو",
                "سرچ رزلٹ کھولو",
                "یہ سرچ رزلٹ کھولو",
                "نتیجہ کھولو",
            ),

            "path_exists": (
                "پاتھ چیک کرو",
                "کیا یہ پاتھ موجود ہے",
                "کیا یہ راستہ موجود ہے",
                "راستہ چیک کرو",
            ),

            "list_directory": (
                "ڈائریکٹری دکھاؤ",
                "فائلیں دکھاؤ",
                "فولڈر کا مواد دکھاؤ",
                "فولڈر کے اندر کیا ہے",
                "اس فولڈر میں کیا ہے",
            ),

            "file_info": (
                "فائل کی معلومات",
                "فائل کی تفصیلات",
                "فائل کے بارے میں معلومات",
            ),

            "create_folder": (
                "فولڈر بناؤ",
                "فولڈر بنا دو",
                "نیا فولڈر بناؤ",
                "نیا فولڈر بنا دو",
                "فولڈر تیار کرو",
            ),

            "create_file": (
                "فائل بناؤ",
                "فائل بنا دو",
                "نئی فائل بناؤ",
                "نئی فائل بنا دو",
            ),

            "read_file": (
                "فائل پڑھو",
                "یہ فائل پڑھو",
                "فائل کا مواد دکھاؤ",
                "فائل کے اندر کیا ہے",
            ),

            "copy": (
                "کاپی کرو",
                "اسے کاپی کرو",
                "فائل کاپی کرو",
                "فولڈر کاپی کرو",
            ),

            "move": (
                "منتقل کرو",
                "اسے منتقل کرو",
                "فائل منتقل کرو",
                "فولڈر منتقل کرو",
            ),

            "rename": (
                "نام بدل دو",
                "نام تبدیل کرو",
                "اس کا نام بدل دو",
                "فائل کا نام بدل دو",
                "فولڈر کا نام بدل دو",
            ),

            "search_files": (
                "فائل تلاش کرو",
                "فائل ڈھونڈو",
                "فائلیں تلاش کرو",
                "فائل تلاش کر دو",
            ),

            "open_path": (
                "پاتھ کھولو",
                "یہ پاتھ کھولو",
                "لوکیشن کھولو",
                "یہ لوکیشن کھولو",
            ),

            "open_in_explorer": (
                "ایکسپلورر میں کھولو",
                "ایکسپلورر میں دکھاؤ",
                "فولڈر ایکسپلورر میں کھولو",
            ),

            "search": (
                "تلاش کرو",
                "تلاش کر دو",
                "گوگل پر تلاش کرو",
                "گوگل کرو",
                "ڈھونڈو",
                "تلاش کریں",
            ),

            "youtube_search": (
                "یوٹیوب کھولو",
                "یوٹیوب پر تلاش کرو",
                "یوٹیوب پر دیکھو",
                "یوٹیوب پر چلاؤ",
                "یوٹیوب پر ویڈیو چلاؤ",
            ),

            "time": (
                "وقت کیا ہے",
                "ابھی کیا وقت ہے",
                "اس وقت کیا بجے ہیں",
                "کتنے بجے ہیں",
                "موجودہ وقت کیا ہے",
                "ٹائم کیا ہے",
                "ابھی ٹائم کیا ہے",
                "مجھے وقت بتاؤ",
            ),

            "weather": (
                "موسم کیسا ہے",
                "آج موسم کیسا ہے",
                "موجودہ موسم کیا ہے",
                "آج کا موسم بتاؤ",
                "موسم بتاؤ",
            ),

            "identity": (
                "تم کون ہو",
                "آپ کون ہیں",
                "آپ کیا ہیں",
                "آپ کا نام کیا ہے",
                "جارویس کون ہے",
                "اپنے بارے میں بتاؤ",
            ),
        },

        # =====================================================
        # ROMAN URDU
        # =====================================================

        "Roman Urdu": {

            "open": (
                "kholo",
                "khol do",
                "khol dein",
                "khol dena",
                "chalao",
                "chala do",
                "chala dein",
                "shuru karo",
                "shuru kar do",
                "shuru karein",
                "on karo",
                "on kar do",
                "on karein",
            ),

            "close": (
                "band karo",
                "band kar do",
                "band karein",
                "band kar dein",
                "isko band karo",
                "use band karo",
                "khatam karo",
                "khatam kar do",
            ),

            "close_last": (
                "aakhri app band karo",
                "aakhri app band kar do",
                "aakhri app band karein",
                "pichli app band karo",
                "pichli app band kar do",
                "pichli app band karein",
                "aakhri program band karo",
                "pichla program band karo",
            ),

            "list_windows": (
                "windows dikhao",
                "windows dikha do",
                "windows dikha dein",
                "saari windows dikhao",
                "khuli windows dikhao",
                "khuli hui windows dikhao",
                "kaunsi windows khuli hain",
                "kaunsi windows open hain",
                "kaunsi apps khuli hain",
                "kaunsi apps chal rahi hain",
                "open apps dikhao",
                "running apps dikhao",
            ),

            "active_window": (
                "active window kaunsi hai",
                "active window kya hai",
                "active window dikhao",
                "current window kaunsi hai",
                "current window kya hai",
                "abhi kaunsi window khuli hai",
                "is waqt kaunsi window khuli hai",
                "active app kaunsi hai",
                "kaunsi app active hai",
            ),

            "find_window": (
                "window dhoondo",
                "window dhoondho",
                "window dhoond do",
                "window talaash karo",
                "window talaash kar do",
                "window ka pata lagao",
                "window locate karo",
                "app window dhoondo",
            ),

            "focus_window": (
                "focus karo",
                "window focus karo",
                "window par jao",
                "is window par jao",
                "window saamne lao",
                "window ko saamne lao",
                "window aage lao",
                "window ko aage lao",
                "window ko front par lao",
            ),

            "close_window": (
                "window band karo",
                "ye window band karo",
                "is window ko band karo",
                "window band kar do",
                "ye window band kar do",
            ),

            "minimize_window": (
                "window choti karo",
                "window choti kar do",
                "window choti karein",
                "is window ko chota karo",
                "window neeche karo",
            ),

            "maximize_window": (
                "window bari karo",
                "window bari kar do",
                "window bari karein",
                "is window ko bara karo",
                "window full screen karo",
                "window ko full screen karo",
            ),

            "restore_window": (
                "window restore karo",
                "window restore kar do",
                "window wapas normal karo",
                "window normal karo",
                "window ka size wapas karo",
            ),

            "minimize_active_window": (
                "active window choti karo",
                "active window choti kar do",
                "current window choti karo",
                "current window choti kar do",
                "active window minimize karo",
                "current window minimize karo",
            ),

            "maximize_active_window": (
                "active window bari karo",
                "active window bari kar do",
                "current window bari karo",
                "current window bari kar do",
                "active window maximize karo",
                "current window maximize karo",
            ),

            "restore_active_window": (
                "active window normal karo",
                "active window wapas normal karo",
                "current window normal karo",
                "current window wapas normal karo",
                "active window restore karo",
                "current window restore karo",
            ),

            "minimize_active_window": (
                "active window minimize karo",
                "current window minimize karo",
                "active window choti karo",
            ),

            "maximize_active_window": (
                "active window maximize karo",
                "current window maximize karo",
                "active window bari karo",
            ),

            "restore_active_window": (
                "active window restore karo",
                "current window restore karo",
                "active window wapas normal karo",
            ),

            "mouse_position": (
                "mouse ki position",
                "mouse kahan hai",
                "mouse kahan mojood hai",
                "cursor kahan hai",
                "cursor ki position",
                "cursor ki jagah batao",
                "mouse ki jagah batao",
                "mouse ki position batao",
                "cursor ki position batao",
                "mouse ki location batao",
            ),

            "mouse_move": (
                "mouse move karo",
                "mouse hilaao",
                "mouse le jao",
                "mouse ko le jao",
                "cursor move karo",
                "cursor hilaao",
                "cursor le jao",
                "cursor ko le jao",
                "mouse yahan le jao",
                "mouse wahan le jao",
                "cursor yahan le jao",
                "cursor wahan le jao",
            ),

            "mouse_click": (
                "click karo",
                "click kar do",
                "mouse click karo",
                "left click karo",
                "left click kar do",
                "yahan click karo",
                "wahan click karo",
                "is par click karo",
                "idhar click karo",
                "udhar click karo",
            ),

            "mouse_double_click": (
                "double click karo",
                "double click kar do",
                "mouse double click karo",
                "yahan double click karo",
                "wahan double click karo",
                "is par double click karo",
            ),

            "mouse_right_click": (
                "right click karo",
                "right click kar do",
                "daen click karo",
                "daein click karo",
                "mouse par right click karo",
                "yahan right click karo",
                "wahan right click karo",
            ),

            "mouse_middle_click": (
                "middle click karo",
                "middle click kar do",
                "darmiyani click karo",
                "mouse par middle click karo",
            ),

            "mouse_scroll": (
                "scroll karo",
                "scroll kar do",
                "upar scroll karo",
                "upar scroll kar do",
                "neeche scroll karo",
                "neeche scroll kar do",
                "upar ki taraf scroll karo",
                "neeche ki taraf scroll karo",
                "mouse scroll karo",
            ),

            "keyboard_type": (
                "ye likho",
                "ye likh do",
                "ye type karo",
                "ye type kar do",
                "matn likho",
                "matn type karo",
                "ye text likho",
                "ye text type karo",
                "ye text enter karo",
            ),

            "keyboard_press": (
                "dabao",
                "key dabao",
                "key dabayein",
                "ye key dabao",
                "ye key dabayein",
                "button dabao",
                "button dabayein",
                "ye button dabao",
                "key daba do",
            ),

            "keyboard_hotkey": (
                "keyboard shortcut",
                "keyboard ka shortcut",
                "shortcut dabao",
                "shortcut dabayein",
                "shortcut use karo",
                "shortcut istemal karo",
                "keyboard shortcut dabao",
                "keyboard shortcut use karo",
            ),

            "ui_find": (
                "button talash karo",
                "button talash kar do",
                "control talash karo",
                "element talash karo",
                "is button ko talash karo",
                "is control ko talash karo",
                "is element ko talash karo",
                "button dhoondo",
                "control dhoondo",
                "element dhoondo",
            ),

            "ui_click": (
                "button par click karo",
                "button click karo",
                "control par click karo",
                "element par click karo",
                "is button par click karo",
                "is control par click karo",
                "is element par click karo",
            ),

            "ui_find_descriptor": (
                "is naam ka button talash karo",
                "is naam wala button talash karo",
                "is naam ka control talash karo",
                "is naam wala control talash karo",
                "is naam ka element talash karo",
                "is naam wala element talash karo",
            ),

            "ui_click_descriptor": (
                "is naam wale button par click karo",
                "is naam ka button click karo",
                "is naam wale control par click karo",
                "is naam ka control click karo",
                "is naam wale element par click karo",
            ),

            "ui_type_descriptor": (
                "field mein likho",
                "field mein ye likho",
                "box mein likho",
                "box mein ye likho",
                "field mein text likho",
                "box mein text dalo",
                "is field mein likho",
            ),

            "ui_focus": (
                "window par focus karo",
                "window ko focus karo",
                "application par focus karo",
                "app par focus karo",
                "control par focus karo",
                "is window par focus karo",
                "is app par focus karo",
            ),

            "ui_click_at": (
                "yahan click karo",
                "is jagah click karo",
                "coordinate par click karo",
                "is coordinate par click karo",
                "position par click karo",
            ),

            "ui_describe": (
                "is window ki tafseel batao",
                "window ki tafseel batao",
                "is screen ki tafseel batao",
                "screen ki tafseel batao",
                "current window ki tafseel batao",
                "screen par kya hai",
                "is window mein kya hai",
            ),

            "ui_type": (
                "yahan likho",
                "yahan type karo",
                "field mein likho",
                "box mein likho",
                "ye text likho",
                "ye text enter karo",
            ),

            "search_ui": (
                "screen mein talash karo",
                "window mein talash karo",
                "interface mein talash karo",
                "screen par talash karo",
                "window mein dhoondo",
            ),

            "open_search_result": (
                "search result kholo",
                "search ka result kholo",
                "ye search result kholo",
                "result kholo",
            ),

            "path_exists": (
                "path check karo",
                "kya ye path mojood hai",
                "ye path available hai",
                "raasta check karo",
            ),

            "list_directory": (
                "directory dikhao",
                "files dikhao",
                "folder ka content dikhao",
                "folder ke andar kya hai",
                "is folder mein kya hai",
            ),

            "file_info": (
                "file ki maloomat",
                "file ki tafseel",
                "file ke bare mein maloomat",
            ),

            "create_folder": (
                "folder banao",
                "folder bana do",
                "naya folder banao",
                "naya folder bana do",
                "folder tayar karo",
            ),

            "create_file": (
                "file banao",
                "file bana do",
                "nayi file banao",
                "nayi file bana do",
            ),

            "read_file": (
                "file parho",
                "ye file parho",
                "file ka content dikhao",
                "file ke andar kya hai",
            ),

            "copy": (
                "copy karo",
                "isko copy karo",
                "file copy karo",
                "folder copy karo",
            ),

            "move": (
                "move karo",
                "isko move karo",
                "file move karo",
                "folder move karo",
            ),

            "rename": (
                "naam badal do",
                "naam tabdeel karo",
                "iska naam badal do",
                "file ka naam badal do",
                "folder ka naam badal do",
            ),

            "search_files": (
                "file dhoondo",
                "file talaash karo",
                "files dhoondo",
                "file search karo",
            ),

            "open_path": (
                "path kholo",
                "ye path kholo",
                "location kholo",
                "ye location kholo",
            ),

            "open_in_explorer": (
                "explorer mein kholo",
                "explorer mein dikhao",
                "folder explorer mein kholo",
            ),

            "search": (
                "search karo",
                "talash karo",
                "talash kar do",
                "google par search karo",
                "google karo",
                "dhoondo",
                "dhondho",
            ),

            "youtube_search": (
                "youtube kholo",
                "youtube par search karo",
                "youtube par dekho",
                "youtube par chalao",
                "youtube par video chalao",
            ),

            "time": (
                "waqt kya hai",
                "abhi kya waqt hai",
                "is waqt kya bajay hain",
                "kitne bajay hain",
                "maujooda waqt kya hai",
                "time kya hai",
                "abhi time kya hai",
                "mujhe waqt batao",
            ),

            "weather": (
                "mosam kaisa hai",
                "aaj mosam kaisa hai",
                "maujooda mosam kya hai",
                "aaj ka mosam batao",
                "mosam batao",
            ),

            "identity": (
                "tum kaun ho",
                "aap kaun hain",
                "aap kya hain",
                "aap ka naam kya hai",
                "jarvis kaun hai",
                "apne bare mein batao",
            ),
        },

        # =====================================================
        # HINDI
        # =====================================================

        "Hindi": {

            "open": (
                "खोलो",
                "खोल दो",
                "खोलिए",
                "चलाो",
                "चलाओ",
                "चला दो",
                "चला दीजिए",
                "शुरू करो",
                "शुरू कर दो",
                "ऑन करो",
                "ऑन कर दो",
            ),

            "close": (
                "बंद करो",
                "बंद कर दो",
                "बंद करिए",
                "बंद कर दें",
                "इसे बंद करो",
                "उसको बंद करो",
                "खत्म करो",
                "खत्म कर दो",
            ),

            "close_last": (
                "आखिरी ऐप बंद करो",
                "आखिरी ऐप बंद कर दो",
                "आखिरी ऐप बंद करिए",
                "पिछला ऐप बंद करो",
                "पिछला ऐप बंद कर दो",
                "पिछली ऐप बंद करो",
                "आखिरी प्रोग्राम बंद करो",
            ),

            "list_windows": (
                "विंडोज दिखाओ",
                "विंडोज़ दिखाओ",
                "विंडोज दिखा दो",
                "सारी विंडोज दिखाओ",
                "खुली हुई विंडोज दिखाओ",
                "कौन सी विंडोज खुली हैं",
                "कौन सी विंडोज ओपन हैं",
                "कौन सी ऐप्स खुली हैं",
                "कौन सी ऐप्स चल रही हैं",
                "खुली ऐप्स दिखाओ",
                "चल रही ऐप्स दिखाओ",
            ),

            "active_window": (
                "एक्टिव विंडो कौन सी है",
                "एक्टिव विंडो क्या है",
                "सक्रिय विंडो कौन सी है",
                "मौजूदा विंडो कौन सी है",
                "मौजूदा विंडो क्या है",
                "अभी कौन सी विंडो खुली है",
                "इस समय कौन सी विंडो खुली है",
                "एक्टिव ऐप कौन सी है",
                "कौन सी ऐप एक्टिव है",
            ),

            "find_window": (
                "विंडो ढूंढो",
                "विंडो ढूंढ दो",
                "विंडो खोजो",
                "विंडो खोज दो",
                "विंडो का पता लगाओ",
                "ऐप की विंडो ढूंढो",
            ),

            "focus_window": (
                "फोकस करो",
                "विंडो फोकस करो",
                "विंडो पर जाओ",
                "इस विंडो पर जाओ",
                "विंडो सामने लाओ",
                "विंडो को सामने लाओ",
                "विंडो आगे लाओ",
                "विंडो को आगे लाओ",
                "विंडो को सामने करो",
            ),

            "close_window": (
                "विंडो बंद करो",
                "यह विंडो बंद करो",
                "इस विंडो को बंद करो",
                "विंडो बंद कर दो",
                "यह विंडो बंद कर दो",
            ),

            "minimize_window": (
                "विंडो मिनिमाइज़ करो",
                "विंडो मिनिमाइज़ कर दो",
                "विंडो छोटी करो",
                "विंडो छोटी कर दो",
                "इस विंडो को छोटा करो",
            ),

            "maximize_window": (
                "विंडो मैक्सिमाइज़ करो",
                "विंडो मैक्सिमाइज़ कर दो",
                "विंडो बड़ी करो",
                "विंडो बड़ी कर दो",
                "इस विंडो को बड़ा करो",
                "विंडो फुल स्क्रीन करो",
            ),

            "restore_window": (
                "विंडो रिस्टोर करो",
                "विंडो रिस्टोर कर दो",
                "विंडो वापस सामान्य करो",
                "विंडो नॉर्मल करो",
                "इस विंडो को सामान्य करो",
            ),

            "minimize_active_window": (
                "सक्रिय विंडो छोटी करो",
                "सक्रिय विंडो छोटी कर दो",
                "मौजूदा विंडो छोटी करो",
                "मौजूदा विंडो छोटी कर दो",
                "एक्टिव विंडो मिनिमाइज़ करो",
            ),

            "maximize_active_window": (
                "सक्रिय विंडो बड़ी करो",
                "सक्रिय विंडो बड़ी कर दो",
                "मौजूदा विंडो बड़ी करो",
                "मौजूदा विंडो बड़ी कर दो",
                "एक्टिव विंडो मैक्सिमाइज़ करो",
            ),

            "restore_active_window": (
                "सक्रिय विंडो वापस सामान्य करो",
                "सक्रिय विंडो सामान्य करो",
                "मौजूदा विंडो वापस सामान्य करो",
                "मौजूदा विंडो सामान्य करो",
                "एक्टिव विंडो रिस्टोर करो",
            ),

            "mouse_position": (
                "माउस की पोज़िशन",
                "माउस कहाँ है",
                "माउस कहाँ मौजूद है",
                "कर्सर कहाँ है",
                "कर्सर की पोज़िशन",
                "कर्सर की जगह बताओ",
                "माउस की जगह बताओ",
                "माउस की पोज़िशन बताओ",
                "कर्सर की पोज़िशन बताओ",
            ),

            "mouse_move": (
                "माउस हिलाओ",
                "माउस वहाँ ले जाओ",
                "माउस यहाँ ले जाओ",
                "माउस को वहाँ ले जाओ",
                "कर्सर हिलाओ",
                "कर्सर वहाँ ले जाओ",
                "कर्सर यहाँ ले जाओ",
                "कर्सर को वहाँ ले जाओ",
                "माउस मूव करो",
                "कर्सर मूव करो",
            ),

            "mouse_click": (
                "क्लिक करो",
                "क्लिक कर दो",
                "माउस क्लिक करो",
                "लेफ्ट क्लिक करो",
                "लेफ्ट क्लिक कर दो",
                "यहाँ क्लिक करो",
                "वहाँ क्लिक करो",
                "इस पर क्लिक करो",
                "इधर क्लिक करो",
                "उधर क्लिक करो",
            ),

            "mouse_double_click": (
                "डबल क्लिक करो",
                "डबल क्लिक कर दो",
                "माउस डबल क्लिक करो",
                "यहाँ डबल क्लिक करो",
                "वहाँ डबल क्लिक करो",
                "इस पर डबल क्लिक करो",
            ),

            "mouse_right_click": (
                "राइट क्लिक करो",
                "राइट क्लिक कर दो",
                "दायाँ क्लिक करो",
                "दायाँ क्लिक कर दो",
                "माउस पर राइट क्लिक करो",
                "यहाँ राइट क्लिक करो",
                "वहाँ राइट क्लिक करो",
            ),

            "mouse_middle_click": (
                "मिडिल क्लिक करो",
                "मिडिल क्लिक कर दो",
                "बीच वाला क्लिक करो",
                "माउस पर मिडिल क्लिक करो",
            ),

            "mouse_scroll": (
                "स्क्रॉल करो",
                "स्क्रॉल कर दो",
                "ऊपर स्क्रॉल करो",
                "ऊपर स्क्रॉल कर दो",
                "नीचे स्क्रॉल करो",
                "नीचे स्क्रॉल कर दो",
                "ऊपर की तरफ स्क्रॉल करो",
                "नीचे की तरफ स्क्रॉल करो",
                "माउस स्क्रॉल करो",
            ),

            "keyboard_type": (
                "यह लिखो",
                "यह लिख दो",
                "यह टाइप करो",
                "यह टाइप कर दो",
                "टेक्स्ट लिखो",
                "टेक्स्ट टाइप करो",
                "यह टेक्स्ट डालो",
                "यह टेक्स्ट लिखो",
            ),

            "keyboard_press": (
                "दबाओ",
                "की दबाओ",
                "की दबा दो",
                "यह की दबाओ",
                "यह की दबा दो",
                "बटन दबाओ",
                "बटन दबा दो",
                "यह बटन दबाओ",
            ),

            "keyboard_hotkey": (
                "कीबोर्ड शॉर्टकट",
                "कीबोर्ड का शॉर्टकट",
                "शॉर्टकट दबाओ",
                "शॉर्टकट दबा दो",
                "शॉर्टकट इस्तेमाल करो",
                "कीबोर्ड शॉर्टकट दबाओ",
            ),

            "ui_find": (
                "बटन खोजो",
                "बटन ढूँढो",
                "कंट्रोल खोजो",
                "एलिमेंट खोजो",
                "इस बटन को खोजो",
                "इस कंट्रोल को खोजो",
                "इस एलिमेंट को खोजो",
                "बटन ढूँढ कर बताओ",
            ),
            
            "ui_click": (
                "बटन पर क्लिक करो",
                "बटन क्लिक करो",
                "कंट्रोल पर क्लिक करो",
                "एलिमेंट पर क्लिक करो",
                "इस बटन पर क्लिक करो",
                "इस कंट्रोल पर क्लिक करो",
                "इस एलिमेंट पर क्लिक करो",
            ),
            
            "ui_find_descriptor": (
                "इस नाम का बटन खोजो",
                "इस नाम वाला बटन खोजो",
                "इस नाम का कंट्रोल खोजो",
                "इस नाम वाला कंट्रोल खोजो",
                "इस नाम का एलिमेंट खोजो",
                "इस नाम वाला एलिमेंट खोजो",
            ),
            
            "ui_click_descriptor": (
                "इस नाम वाले बटन पर क्लिक करो",
                "इस नाम के बटन पर क्लिक करो",
                "इस नाम वाले कंट्रोल पर क्लिक करो",
                "इस नाम के कंट्रोल पर क्लिक करो",
                "इस नाम वाले एलिमेंट पर क्लिक करो",
            ),
            
            "ui_type_descriptor": (
                "फील्ड में लिखो",
                "फील्ड में यह लिखो",
                "बॉक्स में लिखो",
                "बॉक्स में यह लिखो",
                "फील्ड में टेक्स्ट लिखो",
                "बॉक्स में टेक्स्ट डालो",
                "इस फील्ड में लिखो",
            ),
            
            "ui_focus": (
                "विंडो पर फोकस करो",
                "विंडो को फोकस करो",
                "एप्लिकेशन पर फोकस करो",
                "ऐप पर फोकस करो",
                "कंट्रोल पर फोकस करो",
                "इस विंडो पर फोकस करो",
                "इस ऐप पर फोकस करो",
            ),
            
            "ui_click_at": (
                "यहाँ क्लिक करो",
                "इस जगह क्लिक करो",
                "कोऑर्डिनेट पर क्लिक करो",
                "इस कोऑर्डिनेट पर क्लिक करो",
                "पोज़िशन पर क्लिक करो",
            ),
            
            "ui_describe": (
                "इस विंडो की जानकारी बताओ",
                "विंडो की जानकारी बताओ",
                "इस स्क्रीन की जानकारी बताओ",
                "स्क्रीन की जानकारी बताओ",
                "वर्तमान विंडो की जानकारी बताओ",
                "स्क्रीन पर क्या है",
                "इस विंडो में क्या है",
            ),
            
            "ui_type": (
                "यहाँ लिखो",
                "यहाँ टाइप करो",
                "फील्ड में लिखो",
                "बॉक्स में लिखो",
                "यह टेक्स्ट लिखो",
                "यह टेक्स्ट डालो",
            ),
            
            "search_ui": (
                "स्क्रीन में खोजो",
                "विंडो में खोजो",
                "इंटरफेस में खोजो",
                "स्क्रीन पर खोजो",
                "इस विंडो में ढूँढो",
            ),
            
            "open_search_result": (
                "सर्च रिजल्ट खोलो",
                "सर्च का रिजल्ट खोलो",
                "यह सर्च रिजल्ट खोलो",
                "रिजल्ट खोलो",
            ),

            "path_exists": (
                "पाथ चेक करो",
                "क्या यह पाथ मौजूद है",
            ),

            "list_directory": (
                "डायरेक्टरी दिखाओ",
                "फ़ाइलें दिखाओ",
                "फ़ोल्डर के अंदर क्या है",
                "फ़ोल्डर का सामग्री दिखाओ",
            ),

            "file_info": (
                "फ़ाइल की जानकारी",
                "फ़ाइल की डिटेल",
                "फ़ाइल के बारे में बताओ",
            ),

            "create_folder": (
                "फ़ोल्डर बनाओ",
                "फ़ोल्डर बना दो",
                "नया फ़ोल्डर बनाओ",
                "नया फ़ोल्डर बना दो",
            ),

            "create_file": (
                "फ़ाइल बनाओ",
                "फ़ाइल बना दो",
                "नई फ़ाइल बनाओ",
                "नई फ़ाइल बना दो",
            ),

            "read_file": (
                "फ़ाइल पढ़ो",
                "यह फ़ाइल पढ़ो",
                "फ़ाइल की सामग्री दिखाओ",
            ),

            "copy": (
                "कॉपी करो",
                "इसे कॉपी करो",
                "फ़ाइल कॉपी करो",
                "फ़ोल्डर कॉपी करो",
            ),

            "move": (
                "इसे ले जाओ",
                "फ़ाइल ले जाओ",
                "फ़ोल्डर ले जाओ",
                "स्थानांतरित करो",
            ),

            "rename": (
                "नाम बदलो",
                "नाम बदल दो",
                "फ़ाइल का नाम बदलो",
                "फ़ोल्डर का नाम बदलो",
            ),

            "search_files": (
                "फ़ाइल ढूंढो",
                "फ़ाइल खोजो",
                "फ़ाइलें खोजो",
            ),

            "open_path": (
                "पाथ खोलो",
                "यह पाथ खोलो",
                "लोकेशन खोलो",
            ),

            "open_in_explorer": (
                "एक्सप्लोरर में खोलो",
                "एक्सप्लोरर में दिखाओ",
                "फ़ोल्डर एक्सप्लोरर में खोलो",
            ),

            "search": (
                "खोजो",
                "खोज करो",
                "गूगल पर खोजो",
                "ढूंढो",
                "सर्च करो",
            ),

            "youtube_search": (
                "यूट्यूब खोलो",
                "यूट्यूब पर खोजो",
                "यूट्यूब पर चलाओ",
                "यूट्यूब पर वीडियो चलाओ",
            ),

            "time": (
                "समय क्या है",
                "अभी क्या समय है",
                "अभी कितने बजे हैं",
                "कितने बजे हैं",
                "वर्तमान समय क्या है",
                "टाइम क्या है",
            ),

            "weather": (
                "मौसम कैसा है",
                "आज मौसम कैसा है",
                "मौजूदा मौसम क्या है",
                "आज का मौसम बताओ",
            ),

            "identity": (
                "तुम कौन हो",
                "आप कौन हैं",
                "आप क्या हैं",
                "आपका नाम क्या है",
                "जार्विस कौन है",
                "अपने बारे में बताओ",
            ),
        },

        # =====================================================
        # PUNJABI
        # =====================================================

        "Punjabi": {

            "open": (
                "ਖੋਲ੍ਹੋ",
                "ਖੋਲ੍ਹ ਦਿਓ",
                "ਖੋਲ੍ਹ ਦੇਵੋ",
                "ਚਲਾਓ",
                "ਚਲਾ ਦਿਓ",
                "ਚਲਾ ਦੇਵੋ",
                "ਸ਼ੁਰੂ ਕਰੋ",
                "ਸ਼ੁਰੂ ਕਰ ਦਿਓ",
                "ਆਨ ਕਰੋ",
                "ਆਨ ਕਰ ਦਿਓ",
            ),
            
            "close": (
                "ਬੰਦ ਕਰੋ",
                "ਬੰਦ ਕਰ ਦਿਓ",
                "ਬੰਦ ਕਰ ਦੇਵੋ",
                "ਇਸਨੂੰ ਬੰਦ ਕਰੋ",
                "ਉਸਨੂੰ ਬੰਦ ਕਰੋ",
                "ਖਤਮ ਕਰੋ",
                "ਖਤਮ ਕਰ ਦਿਓ",
            ),
            
            "close_last": (
                "ਆਖਰੀ ਐਪ ਬੰਦ ਕਰੋ",
                "ਆਖਰੀ ਐਪ ਬੰਦ ਕਰ ਦਿਓ",
                "ਆਖਰੀ ਐਪ ਬੰਦ ਕਰ ਦੇਵੋ",
                "ਪਿਛਲੀ ਐਪ ਬੰਦ ਕਰੋ",
                "ਪਿਛਲੀ ਐਪ ਬੰਦ ਕਰ ਦਿਓ",
                "ਆਖਰੀ ਪ੍ਰੋਗਰਾਮ ਬੰਦ ਕਰੋ",
            ),
            
            "list_windows": (
                "ਵਿੰਡੋਜ਼ ਦਿਖਾਓ",
                "ਵਿੰਡੋਜ਼ ਦਿਖਾ ਦਿਓ",
                "ਸਾਰੀਆਂ ਵਿੰਡੋਜ਼ ਦਿਖਾਓ",
                "ਖੁੱਲ੍ਹੀਆਂ ਵਿੰਡੋਜ਼ ਦਿਖਾਓ",
                "ਕਿਹੜੀਆਂ ਵਿੰਡੋਜ਼ ਖੁੱਲ੍ਹੀਆਂ ਹਨ",
                "ਕਿਹੜੀਆਂ ਵਿੰਡੋਜ਼ ਓਪਨ ਹਨ",
                "ਕਿਹੜੀਆਂ ਐਪਾਂ ਖੁੱਲ੍ਹੀਆਂ ਹਨ",
                "ਕਿਹੜੀਆਂ ਐਪਾਂ ਚੱਲ ਰਹੀਆਂ ਹਨ",
                "ਖੁੱਲ੍ਹੀਆਂ ਐਪਾਂ ਦਿਖਾਓ",
            ),
            
            "active_window": (
                "ਐਕਟਿਵ ਵਿੰਡੋ ਕਿਹੜੀ ਹੈ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਕੀ ਹੈ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਕਿਹੜੀ ਹੈ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਕੀ ਹੈ",
                "ਹੁਣ ਕਿਹੜੀ ਵਿੰਡੋ ਖੁੱਲ੍ਹੀ ਹੈ",
                "ਇਸ ਵੇਲੇ ਕਿਹੜੀ ਵਿੰਡੋ ਖੁੱਲ੍ਹੀ ਹੈ",
                "ਐਕਟਿਵ ਐਪ ਕਿਹੜੀ ਹੈ",
                "ਕਿਹੜੀ ਐਪ ਐਕਟਿਵ ਹੈ",
            ),
            
            "find_window": (
                "ਵਿੰਡੋ ਲੱਭੋ",
                "ਵਿੰਡੋ ਲੱਭ ਦਿਓ",
                "ਵਿੰਡੋ ਖੋਜੋ",
                "ਵਿੰਡੋ ਦਾ ਪਤਾ ਲਗਾਓ",
                "ਐਪ ਦੀ ਵਿੰਡੋ ਲੱਭੋ",
            ),
            
            "focus_window": (
                "ਫੋਕਸ ਕਰੋ",
                "ਵਿੰਡੋ ਫੋਕਸ ਕਰੋ",
                "ਵਿੰਡੋ ਤੇ ਜਾਓ",
                "ਇਸ ਵਿੰਡੋ ਤੇ ਜਾਓ",
                "ਵਿੰਡੋ ਸਾਹਮਣੇ ਲਿਆਓ",
                "ਵਿੰਡੋ ਨੂੰ ਸਾਹਮਣੇ ਲਿਆਓ",
                "ਵਿੰਡੋ ਅੱਗੇ ਲਿਆਓ",
                "ਵਿੰਡੋ ਨੂੰ ਅੱਗੇ ਲਿਆਓ",
            ),
            
            "close_window": (
                "ਵਿੰਡੋ ਬੰਦ ਕਰੋ",
                "ਇਹ ਵਿੰਡੋ ਬੰਦ ਕਰੋ",
                "ਇਸ ਵਿੰਡੋ ਨੂੰ ਬੰਦ ਕਰੋ",
                "ਵਿੰਡੋ ਬੰਦ ਕਰ ਦਿਓ",
                "ਇਹ ਵਿੰਡੋ ਬੰਦ ਕਰ ਦਿਓ",
            ),
            
            "minimize_window": (
                "ਵਿੰਡੋ ਮਿਨਿਮਾਈਜ਼ ਕਰੋ",
                "ਵਿੰਡੋ ਮਿਨਿਮਾਈਜ਼ ਕਰ ਦਿਓ",
                "ਵਿੰਡੋ ਛੋਟੀ ਕਰੋ",
                "ਵਿੰਡੋ ਛੋਟੀ ਕਰ ਦਿਓ",
                "ਇਸ ਵਿੰਡੋ ਨੂੰ ਛੋਟਾ ਕਰੋ",
            ),
            
            "maximize_window": (
                "ਵਿੰਡੋ ਮੈਕਸੀਮਾਈਜ਼ ਕਰੋ",
                "ਵਿੰਡੋ ਮੈਕਸੀਮਾਈਜ਼ ਕਰ ਦਿਓ",
                "ਵਿੰਡੋ ਵੱਡੀ ਕਰੋ",
                "ਵਿੰਡੋ ਵੱਡੀ ਕਰ ਦਿਓ",
                "ਇਸ ਵਿੰਡੋ ਨੂੰ ਵੱਡਾ ਕਰੋ",
                "ਵਿੰਡੋ ਫੁੱਲ ਸਕ੍ਰੀਨ ਕਰੋ",
            ),
            
            "restore_window": (
                "ਵਿੰਡੋ ਰੀਸਟੋਰ ਕਰੋ",
                "ਵਿੰਡੋ ਰੀਸਟੋਰ ਕਰ ਦਿਓ",
                "ਵਿੰਡੋ ਵਾਪਸ ਨਾਰਮਲ ਕਰੋ",
                "ਵਿੰਡੋ ਨਾਰਮਲ ਕਰੋ",
                "ਇਸ ਵਿੰਡੋ ਨੂੰ ਨਾਰਮਲ ਕਰੋ",
            ),
            
            "minimize_active_window": (
                "ਐਕਟਿਵ ਵਿੰਡੋ ਛੋਟੀ ਕਰੋ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਛੋਟੀ ਕਰ ਦਿਓ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਛੋਟੀ ਕਰੋ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਛੋਟੀ ਕਰ ਦਿਓ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਮਿਨਿਮਾਈਜ਼ ਕਰੋ",
            ),
            
            "maximize_active_window": (
                "ਐਕਟਿਵ ਵਿੰਡੋ ਵੱਡੀ ਕਰੋ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਵੱਡੀ ਕਰ ਦਿਓ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਵੱਡੀ ਕਰੋ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਵੱਡੀ ਕਰ ਦਿਓ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਮੈਕਸੀਮਾਈਜ਼ ਕਰੋ",
            ),
            
            "restore_active_window": (
                "ਐਕਟਿਵ ਵਿੰਡੋ ਵਾਪਸ ਨਾਰਮਲ ਕਰੋ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਨਾਰਮਲ ਕਰੋ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਵਾਪਸ ਨਾਰਮਲ ਕਰੋ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਨਾਰਮਲ ਕਰੋ",
                "ਐਕਟਿਵ ਵਿੰਡੋ ਰੀਸਟੋਰ ਕਰੋ",
            ),

            "mouse_position": (
                "ਮਾਊਸ ਦੀ ਪੋਜ਼ੀਸ਼ਨ",
                "ਮਾਊਸ ਕਿੱਥੇ ਹੈ",
                "ਮਾਊਸ ਕਿੱਥੇ ਮੌਜੂਦ ਹੈ",
                "ਕਰਸਰ ਕਿੱਥੇ ਹੈ",
                "ਕਰਸਰ ਦੀ ਪੋਜ਼ੀਸ਼ਨ",
                "ਕਰਸਰ ਦੀ ਜਗ੍ਹਾ ਦੱਸੋ",
                "ਮਾਊਸ ਦੀ ਜਗ੍ਹਾ ਦੱਸੋ",
                "ਮਾਊਸ ਦੀ ਪੋਜ਼ੀਸ਼ਨ ਦੱਸੋ",
                "ਕਰਸਰ ਦੀ ਪੋਜ਼ੀਸ਼ਨ ਦੱਸੋ",
            ),

            "mouse_move": (
                "ਮਾਊਸ ਹਿਲਾਓ",
                "ਮਾਊਸ ਉੱਥੇ ਲੈ ਜਾਓ",
                "ਮਾਊਸ ਇੱਥੇ ਲੈ ਜਾਓ",
                "ਮਾਊਸ ਨੂੰ ਉੱਥੇ ਲੈ ਜਾਓ",
                "ਕਰਸਰ ਹਿਲਾਓ",
                "ਕਰਸਰ ਉੱਥੇ ਲੈ ਜਾਓ",
                "ਕਰਸਰ ਇੱਥੇ ਲੈ ਜਾਓ",
                "ਕਰਸਰ ਨੂੰ ਉੱਥੇ ਲੈ ਜਾਓ",
                "ਮਾਊਸ ਮੂਵ ਕਰੋ",
                "ਕਰਸਰ ਮੂਵ ਕਰੋ",
            ),

            "mouse_click": (
                "ਕਲਿੱਕ ਕਰੋ",
                "ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਮਾਊਸ ਕਲਿੱਕ ਕਰੋ",
                "ਖੱਬਾ ਕਲਿੱਕ ਕਰੋ",
                "ਖੱਬਾ ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਇੱਥੇ ਕਲਿੱਕ ਕਰੋ",
                "ਉੱਥੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਤੇ ਕਲਿੱਕ ਕਰੋ",
            ),

            "mouse_double_click": (
                "ਡਬਲ ਕਲਿੱਕ ਕਰੋ",
                "ਡਬਲ ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਮਾਊਸ ਡਬਲ ਕਲਿੱਕ ਕਰੋ",
                "ਇੱਥੇ ਡਬਲ ਕਲਿੱਕ ਕਰੋ",
                "ਉੱਥੇ ਡਬਲ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਤੇ ਡਬਲ ਕਲਿੱਕ ਕਰੋ",
            ),

            "mouse_right_click": (
                "ਰਾਈਟ ਕਲਿੱਕ ਕਰੋ",
                "ਰਾਈਟ ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਸੱਜਾ ਕਲਿੱਕ ਕਰੋ",
                "ਸੱਜਾ ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਮਾਊਸ ਤੇ ਰਾਈਟ ਕਲਿੱਕ ਕਰੋ",
                "ਇੱਥੇ ਰਾਈਟ ਕਲਿੱਕ ਕਰੋ",
                "ਉੱਥੇ ਰਾਈਟ ਕਲਿੱਕ ਕਰੋ",
            ),

            "mouse_middle_click": (
                "ਮਿਡਲ ਕਲਿੱਕ ਕਰੋ",
                "ਮਿਡਲ ਕਲਿੱਕ ਕਰ ਦਿਓ",
                "ਵਿਚਕਾਰਲਾ ਕਲਿੱਕ ਕਰੋ",
                "ਮਾਊਸ ਤੇ ਮਿਡਲ ਕਲਿੱਕ ਕਰੋ",
            ),

            "mouse_scroll": (
                "ਸਕ੍ਰੋਲ ਕਰੋ",
                "ਸਕ੍ਰੋਲ ਕਰ ਦਿਓ",
                "ਉੱਪਰ ਸਕ੍ਰੋਲ ਕਰੋ",
                "ਉੱਪਰ ਸਕ੍ਰੋਲ ਕਰ ਦਿਓ",
                "ਹੇਠਾਂ ਸਕ੍ਰੋਲ ਕਰੋ",
                "ਹੇਠਾਂ ਸਕ੍ਰੋਲ ਕਰ ਦਿਓ",
                "ਉੱਪਰ ਵੱਲ ਸਕ੍ਰੋਲ ਕਰੋ",
                "ਹੇਠਾਂ ਵੱਲ ਸਕ੍ਰੋਲ ਕਰੋ",
                "ਮਾਊਸ ਸਕ੍ਰੋਲ ਕਰੋ",
            ),

            "keyboard_type": (
                "ਇਹ ਲਿਖੋ",
                "ਇਹ ਲਿਖ ਦਿਓ",
                "ਇਹ ਟਾਈਪ ਕਰੋ",
                "ਇਹ ਟਾਈਪ ਕਰ ਦਿਓ",
                "ਟੈਕਸਟ ਲਿਖੋ",
                "ਟੈਕਸਟ ਟਾਈਪ ਕਰੋ",
                "ਇਹ ਟੈਕਸਟ ਪਾਓ",
                "ਇਹ ਟੈਕਸਟ ਲਿਖੋ",
            ),

            "keyboard_press": (
                "ਦਬਾਓ",
                "ਕੀ ਦਬਾਓ",
                "ਕੀ ਦਬਾ ਦਿਓ",
                "ਇਹ ਕੀ ਦਬਾਓ",
                "ਇਹ ਕੀ ਦਬਾ ਦਿਓ",
                "ਬਟਨ ਦਬਾਓ",
                "ਬਟਨ ਦਬਾ ਦਿਓ",
                "ਇਹ ਬਟਨ ਦਬਾਓ",
            ),

            "keyboard_hotkey": (
                "ਕੀਬੋਰਡ ਸ਼ਾਰਟਕੱਟ",
                "ਕੀਬੋਰਡ ਦਾ ਸ਼ਾਰਟਕੱਟ",
                "ਸ਼ਾਰਟਕੱਟ ਦਬਾਓ",
                "ਸ਼ਾਰਟਕੱਟ ਦਬਾ ਦਿਓ",
                "ਸ਼ਾਰਟਕੱਟ ਵਰਤੋ",
                "ਕੀਬੋਰਡ ਸ਼ਾਰਟਕੱਟ ਦਬਾਓ",
            ),

            "ui_find": (
                "ਬਟਨ ਲੱਭੋ",
                "ਬਟਨ ਲੱਭ ਦਿਓ",
                "ਕੰਟਰੋਲ ਲੱਭੋ",
                "ਐਲੀਮੈਂਟ ਲੱਭੋ",
                "ਇਹ ਬਟਨ ਲੱਭੋ",
                "ਇਹ ਕੰਟਰੋਲ ਲੱਭੋ",
                "ਇਹ ਐਲੀਮੈਂਟ ਲੱਭੋ",
                "ਬਟਨ ਖੋਜੋ",
                "ਕੰਟਰੋਲ ਖੋਜੋ",
                "ਐਲੀਮੈਂਟ ਖੋਜੋ",
            ),
            
            "ui_click": (
                "ਬਟਨ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਬਟਨ ਕਲਿੱਕ ਕਰੋ",
                "ਕੰਟਰੋਲ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਐਲੀਮੈਂਟ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਬਟਨ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਕੰਟਰੋਲ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਐਲੀਮੈਂਟ ਤੇ ਕਲਿੱਕ ਕਰੋ",
            ),
            
            "ui_find_descriptor": (
                "ਇਸ ਨਾਮ ਵਾਲਾ ਬਟਨ ਲੱਭੋ",
                "ਇਸ ਨਾਮ ਦਾ ਬਟਨ ਲੱਭੋ",
                "ਇਸ ਨਾਮ ਵਾਲਾ ਕੰਟਰੋਲ ਲੱਭੋ",
                "ਇਸ ਨਾਮ ਦਾ ਕੰਟਰੋਲ ਲੱਭੋ",
                "ਇਸ ਨਾਮ ਵਾਲਾ ਐਲੀਮੈਂਟ ਲੱਭੋ",
                "ਇਸ ਨਾਮ ਦਾ ਐਲੀਮੈਂਟ ਲੱਭੋ",
            ),
            
            "ui_click_descriptor": (
                "ਇਸ ਨਾਮ ਵਾਲੇ ਬਟਨ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਨਾਮ ਦੇ ਬਟਨ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਨਾਮ ਵਾਲੇ ਕੰਟਰੋਲ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਨਾਮ ਦੇ ਕੰਟਰੋਲ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਨਾਮ ਵਾਲੇ ਐਲੀਮੈਂਟ ਤੇ ਕਲਿੱਕ ਕਰੋ",
            ),
            
            "ui_type_descriptor": (
                "ਫੀਲਡ ਵਿੱਚ ਲਿਖੋ",
                "ਫੀਲਡ ਵਿੱਚ ਇਹ ਲਿਖੋ",
                "ਬਾਕਸ ਵਿੱਚ ਲਿਖੋ",
                "ਬਾਕਸ ਵਿੱਚ ਇਹ ਲਿਖੋ",
                "ਫੀਲਡ ਵਿੱਚ ਟੈਕਸਟ ਲਿਖੋ",
                "ਬਾਕਸ ਵਿੱਚ ਟੈਕਸਟ ਪਾਓ",
                "ਇਸ ਫੀਲਡ ਵਿੱਚ ਲਿਖੋ",
            ),
            
            "ui_focus": (
                "ਵਿੰਡੋ ਤੇ ਫੋਕਸ ਕਰੋ",
                "ਵਿੰਡੋ ਨੂੰ ਫੋਕਸ ਕਰੋ",
                "ਐਪਲੀਕੇਸ਼ਨ ਤੇ ਫੋਕਸ ਕਰੋ",
                "ਐਪ ਤੇ ਫੋਕਸ ਕਰੋ",
                "ਕੰਟਰੋਲ ਤੇ ਫੋਕਸ ਕਰੋ",
                "ਇਸ ਵਿੰਡੋ ਤੇ ਫੋਕਸ ਕਰੋ",
                "ਇਸ ਐਪ ਤੇ ਫੋਕਸ ਕਰੋ",
            ),
            
            "ui_click_at": (
                "ਇੱਥੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਜਗ੍ਹਾ ਕਲਿੱਕ ਕਰੋ",
                "ਕੋਆਰਡੀਨੇਟ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਇਸ ਕੋਆਰਡੀਨੇਟ ਤੇ ਕਲਿੱਕ ਕਰੋ",
                "ਪੋਜ਼ੀਸ਼ਨ ਤੇ ਕਲਿੱਕ ਕਰੋ",
            ),
            
            "ui_describe": (
                "ਇਸ ਵਿੰਡੋ ਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ",
                "ਵਿੰਡੋ ਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ",
                "ਇਸ ਸਕ੍ਰੀਨ ਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ",
                "ਸਕ੍ਰੀਨ ਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ",
                "ਮੌਜੂਦਾ ਵਿੰਡੋ ਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ",
                "ਸਕ੍ਰੀਨ ਤੇ ਕੀ ਹੈ",
                "ਇਸ ਵਿੰਡੋ ਵਿੱਚ ਕੀ ਹੈ",
            ),
            
            "ui_type": (
                "ਇੱਥੇ ਲਿਖੋ",
                "ਇੱਥੇ ਟਾਈਪ ਕਰੋ",
                "ਫੀਲਡ ਵਿੱਚ ਲਿਖੋ",
                "ਬਾਕਸ ਵਿੱਚ ਲਿਖੋ",
                "ਇਹ ਟੈਕਸਟ ਲਿਖੋ",
                "ਇਹ ਟੈਕਸਟ ਪਾਓ",
            ),
            
            "search_ui": (
                "ਸਕ੍ਰੀਨ ਵਿੱਚ ਖੋਜੋ",
                "ਵਿੰਡੋ ਵਿੱਚ ਖੋਜੋ",
                "ਇੰਟਰਫੇਸ ਵਿੱਚ ਖੋਜੋ",
                "ਸਕ੍ਰੀਨ ਤੇ ਖੋਜੋ",
                "ਇਸ ਵਿੰਡੋ ਵਿੱਚ ਲੱਭੋ",
            ),
            
            "open_search_result": (
                "ਸਰਚ ਰਿਜ਼ਲਟ ਖੋਲ੍ਹੋ",
                "ਸਰਚ ਦਾ ਰਿਜ਼ਲਟ ਖੋਲ੍ਹੋ",
                "ਇਹ ਸਰਚ ਰਿਜ਼ਲਟ ਖੋਲ੍ਹੋ",
                "ਰਿਜ਼ਲਟ ਖੋਲ੍ਹੋ",
            ),

            "path_exists": (
                "ਪਾਥ ਚੈੱਕ ਕਰੋ",
                "ਕੀ ਇਹ ਪਾਥ ਮੌਜੂਦ ਹੈ",
            ),

            "list_directory": (
                "ਡਾਇਰੈਕਟਰੀ ਦਿਖਾਓ",
                "ਫਾਇਲਾਂ ਦਿਖਾਓ",
                "ਫੋਲਡਰ ਦੇ ਅੰਦਰ ਕੀ ਹੈ",
                "ਫੋਲਡਰ ਦੀ ਸਮੱਗਰੀ ਦਿਖਾਓ",
            ),

            "file_info": (
                "ਫਾਇਲ ਦੀ ਜਾਣਕਾਰੀ",
                "ਫਾਇਲ ਦੀ ਡੀਟੇਲ",
                "ਇਸ ਫਾਇਲ ਬਾਰੇ ਦੱਸੋ",
            ),

            "create_folder": (
                "ਫੋਲਡਰ ਬਣਾਓ",
                "ਫੋਲਡਰ ਬਣਾ ਦਿਓ",
                "ਨਵਾਂ ਫੋਲਡਰ ਬਣਾਓ",
            ),

            "create_file": (
                "ਫਾਇਲ ਬਣਾਓ",
                "ਫਾਇਲ ਬਣਾ ਦਿਓ",
                "ਨਵੀਂ ਫਾਇਲ ਬਣਾਓ",
            ),

            "read_file": (
                "ਫਾਇਲ ਪੜ੍ਹੋ",
                "ਇਹ ਫਾਇਲ ਪੜ੍ਹੋ",
                "ਫਾਇਲ ਦੀ ਸਮੱਗਰੀ ਦਿਖਾਓ",
            ),

            "copy": (
                "ਕਾਪੀ ਕਰੋ",
                "ਇਸਨੂੰ ਕਾਪੀ ਕਰੋ",
                "ਫਾਇਲ ਕਾਪੀ ਕਰੋ",
                "ਫੋਲਡਰ ਕਾਪੀ ਕਰੋ",
            ),

            "move": (
                "ਮੂਵ ਕਰੋ",
                "ਇਸਨੂੰ ਮੂਵ ਕਰੋ",
                "ਫਾਇਲ ਮੂਵ ਕਰੋ",
                "ਫੋਲਡਰ ਮੂਵ ਕਰੋ",
            ),

            "rename": (
                "ਨਾਮ ਬਦਲੋ",
                "ਨਾਮ ਬਦਲ ਦਿਓ",
                "ਫਾਇਲ ਦਾ ਨਾਮ ਬਦਲੋ",
                "ਫੋਲਡਰ ਦਾ ਨਾਮ ਬਦਲੋ",
            ),

            "search_files": (
                "ਫਾਇਲ ਲੱਭੋ",
                "ਫਾਇਲ ਖੋਜੋ",
                "ਫਾਇਲਾਂ ਲੱਭੋ",
            ),

            "open_path": (
                "ਪਾਥ ਖੋਲ੍ਹੋ",
                "ਇਹ ਪਾਥ ਖੋਲ੍ਹੋ",
                "ਲੋਕੇਸ਼ਨ ਖੋਲ੍ਹੋ",
            ),

            "open_in_explorer": (
                "ਐਕਸਪਲੋਰਰ ਵਿੱਚ ਖੋਲ੍ਹੋ",
                "ਐਕਸਪਲੋਰਰ ਵਿੱਚ ਦਿਖਾਓ",
                "ਫੋਲਡਰ ਐਕਸਪਲੋਰਰ ਵਿੱਚ ਖੋਲ੍ਹੋ",
            ),

            "search": (
                "ਖੋਜੋ",
                "ਖੋਜ ਕਰੋ",
                "ਗੂਗਲ ਤੇ ਖੋਜੋ",
                "ਲੱਭੋ",
                "ਸਰਚ ਕਰੋ",
            ),

            "youtube_search": (
                "ਯੂਟਿਊਬ ਖੋਲ੍ਹੋ",
                "ਯੂਟਿਊਬ ਤੇ ਖੋਜੋ",
                "ਯੂਟਿਊਬ ਤੇ ਚਲਾਓ",
                "ਯੂਟਿਊਬ ਤੇ ਵੀਡੀਓ ਚਲਾਓ",
            ),

            "time": (
                "ਸਮਾਂ ਕੀ ਹੈ",
                "ਹੁਣ ਕਿੰਨੇ ਵਜੇ ਹਨ",
                "ਇਸ ਵੇਲੇ ਕਿੰਨੇ ਵਜੇ ਹਨ",
                "ਕਿੰਨੇ ਵਜੇ ਹਨ",
                "ਮੌਜੂਦਾ ਸਮਾਂ ਕੀ ਹੈ",
                "ਟਾਈਮ ਕੀ ਹੈ",
            ),

            "weather": (
                "ਮੌਸਮ ਕਿਵੇਂ ਹੈ",
                "ਅੱਜ ਮੌਸਮ ਕਿਵੇਂ ਹੈ",
                "ਮੌਜੂਦਾ ਮੌਸਮ ਕੀ ਹੈ",
                "ਅੱਜ ਦਾ ਮੌਸਮ ਦੱਸੋ",
            ),

            "identity": (
                "ਤੁਸੀਂ ਕੌਣ ਹੋ",
                "ਤੁਸੀਂ ਕੀ ਹੋ",
                "ਤੁਹਾਡਾ ਨਾਮ ਕੀ ਹੈ",
                "ਜਾਰਵਿਸ ਕੌਣ ਹੈ",
                "ਆਪਣੇ ਬਾਰੇ ਦੱਸੋ",
            ),
        },
    }

    # =========================================================
    # CANONICAL ACTIONS
    # =========================================================

    ACTIONS = (
        "open",
        "close",
        "close_last",
        "list_windows",
        "active_window",
        "find_window",
        "focus_window",
        "close_window",
        "minimize_window",
        "maximize_window",
        "restore_window",
        "minimize_active_window",
        "maximize_active_window",
        "restore_active_window",
        "mouse_position",
        "mouse_move",
        "mouse_click",
        "mouse_double_click",
        "mouse_right_click",
        "mouse_middle_click",
        "mouse_scroll",
        "keyboard_type",
        "keyboard_press",
        "keyboard_hotkey",
        "ui_find",
        "ui_click",
        "ui_find_descriptor",
        "ui_click_descriptor",
        "ui_type_descriptor",
        "ui_focus",
        "ui_click_at",
        "ui_describe",
        "ui_type",
        "search_ui",
        "open_search_result",
        "path_exists",
        "list_directory",
        "file_info",
        "create_folder",
        "create_file",
        "read_file",
        "copy",
        "move",
        "rename",
        "search_files",
        "open_path",
        "open_in_explorer",
        "search",
        "youtube_search",
        "time",
        "weather",
        "identity",
    )

    # =========================================================
    # LANGUAGE SWITCH DETECTION
    # =========================================================

    @classmethod
    def detect_language_switch(
        cls,
        text: str,
    ) -> Optional[str]:

        if not text:
            return None

        language = (
            language_manager
            .get_primary_language()
        )

        normalized = (
            text.strip()
            .lower()
        )

        phrases = (
            cls.LANGUAGE_SWITCHES
            .get(language, {})
        )

        # Longest phrases first.
        ordered = sorted(
            phrases.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for phrase, target_language in ordered:

            if normalized == phrase:
                return target_language

        return None

    # =========================================================
    # APPLY LANGUAGE SWITCH
    # =========================================================

    @classmethod
    def apply_language_switch(
        cls,
        text: str,
    ) -> Optional[str]:

        requested = (
            cls.detect_language_switch(
                text
            )
        )

        if not requested:
            return None

        if (
            requested
            not in language_manager.active_languages()
        ):
            pass

        success = (
            language_manager
            .set_primary_language(
                requested
            )
        )

        if not success:
            return None

        print(
            "LANGUAGE CHANGED:",
            requested,
        )

        return requested

    # =========================================================
    # APP CANONICALIZATION
    # =========================================================

    @classmethod
    def canonical_app(
        cls,
        text: str,
    ) -> str:

        result = text

        aliases = []

        for canonical, values in (
            cls.APP_ALIASES.items()
        ):

            for value in values:

                aliases.append(
                    (
                        value,
                        canonical,
                    )
                )

        aliases.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for alias, canonical in aliases:

            pattern = re.escape(
                alias
            )

            result = re.sub(
                pattern,
                canonical,
                result,
                flags=re.IGNORECASE,
            )

        return result

    # =========================================================
    # PHRASE REPLACEMENT
    # =========================================================

    @classmethod
    def _replace_selected_language_phrases(
        cls,
        text: str,
        language: str,
    ) -> str:

        result = text.strip()

        language_commands = (
            cls.COMMANDS.get(
                language,
                {}
            )
        )

        replacements = []

        for canonical, phrases in (
            language_commands.items()
        ):

            for phrase in phrases:

                replacements.append(
                    (
                        phrase,
                        canonical,
                    )
                )

        # Longest phrases must be replaced first.
        replacements.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for phrase, canonical in replacements:

            escaped = re.escape(
                phrase
            )

            result = re.sub(
                rf"(?<!\S){escaped}(?!\S)",
                f" {canonical} ",
                result,
                flags=re.IGNORECASE,
            )

        return " ".join(
            result.split()
        )

    # =========================================================
    # ACTION ORDER
    # =========================================================

    @classmethod
    def _fix_action_order(
        cls,
        text: str,
    ) -> str:

        text = " ".join(
            text.split()
        )

        if not text:
            return text

        # Already canonical.
        for action in cls.ACTIONS:

            if text == action:
                return text

            if text.startswith(
                action + " "
            ):
                return text

        words = text.split()

        # Find an action somewhere after the entity.
        for action in cls.ACTIONS:

            if action not in words:
                continue

            index = words.index(action)

            if index == 0:
                return text

            before = words[:index]
            after = words[index + 1:]

            return " ".join(
                [
                    action,
                    *before,
                    *after,
                ]
            )

        return text

    # =========================================================
    # STRICT LANGUAGE VALIDATION
    # =========================================================

    @classmethod
    def is_valid_command_language(
        cls,
        text: str,
    ) -> bool:

        if not text:
            return False

        language = (
            language_manager
            .get_primary_language()
        )

        normalized = (
            text.strip()
            .lower()
        )

        # -----------------------------------------------------
        # English
        # -----------------------------------------------------

        if language == "English":
            return True

        # -----------------------------------------------------
        # Check selected language command phrases
        # -----------------------------------------------------

        commands = cls.COMMANDS.get(
            language,
            {},
        )

        for phrases in commands.values():

            for phrase in phrases:

                if normalized == phrase.lower():
                    return True

                # Phrase exists somewhere in command.
                pattern = (
                    rf"(?<!\S)"
                    rf"{re.escape(phrase.lower())}"
                    rf"(?!\S)"
                )

                if re.search(
                    pattern,
                    normalized,
                ):
                    return True

        # -----------------------------------------------------
        # Language switch is also valid
        # -----------------------------------------------------

        if cls.detect_language_switch(
            text
        ):
            return True

        return False


    # =========================================================
    # NORMALIZE COMMAND
    # =========================================================

    @classmethod
    def canonicalize(
        cls,
        text: str,
    ) -> str:

        if not text:
            return ""

        language = (
            language_manager
            .get_primary_language()
        )

        raw = text.strip()

        if not raw:
            return ""

        # -----------------------------------------------------
        # STRICT LANGUAGE CHECK
        # -----------------------------------------------------

        if not cls.is_valid_command_language(
            raw
        ):

            print(
                "LANGUAGE REJECTED:",
                raw,
                "expected:",
                language,
            )

            return ""

        # -----------------------------------------------------
        # LANGUAGE SWITCH
        # -----------------------------------------------------

        if cls.detect_language_switch(
            raw
        ):

            return (
                "set language to "
                + cls.detect_language_switch(
                    raw
                ).lower()
            )

        # -----------------------------------------------------
        # SELECTED LANGUAGE PHRASES ONLY
        # -----------------------------------------------------

        canonical = (
            cls._replace_selected_language_phrases(
                raw,
                language,
            )
        )

        # -----------------------------------------------------
        # APPLICATION NAMES
        # -----------------------------------------------------

        canonical = cls.canonical_app(
            canonical
        )

        # -----------------------------------------------------
        # CLEANUP
        # -----------------------------------------------------

        canonical = re.sub(
            r"\s+",
            " ",
            canonical,
        ).strip()

        # -----------------------------------------------------
        # ACTION ORDER
        # -----------------------------------------------------

        canonical = cls._fix_action_order(
            canonical
        )

        return canonical

    # =========================================================
    # PREPARE
    # =========================================================

    @classmethod
    def prepare(
        cls,
        text: str,
    ) -> Tuple[str, Optional[str]]:

        if not text:
            return "", None

        requested = (
            cls.detect_language_switch(
                text
            )
        )

        canonical = cls.canonicalize(
            text
        )

        return (
            canonical,
            requested,
        )

    # =========================================================
    # ACTIVE LANGUAGE
    # =========================================================

    @classmethod
    def active_language(cls) -> str:

        return (
            language_manager
            .get_primary_language()
        )


# =============================================================
# GLOBAL INSTANCE
# =============================================================

language_command_adapter = (
    LanguageCommandAdapter()
)