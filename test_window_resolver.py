
from desktop_automation.controller.window_manager import WindowManager
from desktop_automation.resolver.window_resolver import WindowResolver


def main():
    resolver = WindowResolver(WindowManager)

    names = [
        "vs code",
        "vscode",
        "code",
        "visual studio code",
    ]

    print("=" * 60)
    print("WINDOW RESOLVER TEST")
    print("=" * 60)

    for name in names:
        print()
        print(f"SEARCH: {name}")

        window = resolver.resolve(name)

        print("RESULT:", window)


if __name__ == "__main__":
    main()
