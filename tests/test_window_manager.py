
from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.resolver.window_resolver import WindowResolver


def main():
    manager = WindowManager()
    resolver = WindowResolver(manager)

    print("\n=== FIND VS CODE ===")

    window = resolver.resolve("vs code")

    print(window)

    if not window:
        print("VS Code not found.")
        print("\n=== VISIBLE WINDOWS ===")

        for item in manager.list_windows():
            print(item)

        return

    hwnd = window["hwnd"]

    print("\n=== MINIMIZE VS CODE ===")

    success = manager.minimize_window(hwnd)

    print("Success:", success)

    input("\nPress Enter to restore VS Code...")

    print("\n=== RESTORE VS CODE ===")

    success = manager.restore_window(hwnd)

    print("Success:", success)

    input("\nPress Enter to maximize VS Code...")

    print("\n=== MAXIMIZE VS CODE ===")

    success = manager.maximize_window(hwnd)

    print("Success:", success)

    input("\nPress Enter to restore VS Code...")

    print("\n=== RESTORE VS CODE ===")

    success = manager.restore_window(hwnd)

    print("Success:", success)


if __name__ == "__main__":
    main()
