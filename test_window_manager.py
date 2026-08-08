
from automation.desktop.window_manager import WindowManager


def main():
    print("\n=== OPEN WINDOWS ===\n")

    windows = WindowManager.list_windows()

    for window in windows:
        print(
            f"{window['hwnd']} -> {window['title']}"
        )

    print("\n=== ACTIVE WINDOW ===\n")

    active = WindowManager.get_active_window()

    if active:
        print(active)
    else:
        print("No active window found.")

    print("\n=== FIND CHROME ===\n")

    chrome = WindowManager.find_window("chrome")

    if chrome:
        print(chrome)
    else:
        print("Chrome window not found.")


if __name__ == "__main__":
    main()
