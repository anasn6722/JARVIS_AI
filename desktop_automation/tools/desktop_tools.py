from desktop_automation.handler.desktop_handler import DesktopHandler


def register_desktop_tools(registry):
    """Register all desktop automation tools with the tool registry."""

    handler = DesktopHandler()

    registry.register(
        "list_windows",
        "List all visible desktop windows.",
        lambda: handler.handle("list_windows"),
    )

    registry.register(
        "active_window",
        "Get the currently active desktop window.",
        lambda: handler.handle("active_window"),
    )

    registry.register(
        "find_window",
        "Find a desktop window by name.",
        lambda target: handler.handle(
            "find_window",
            target,
        ),
    )

    registry.register(
        "focus_window",
        "Bring a desktop window to the foreground.",
        lambda target: handler.handle(
            "focus_window",
            target,
        ),
    )

    registry.register(
        "minimize_window",
        "Minimize a desktop window.",
        lambda target: handler.handle(
            "minimize_window",
            target,
        ),
    )

    registry.register(
        "maximize_window",
        "Maximize a desktop window.",
        lambda target: handler.handle(
            "maximize_window",
            target,
        ),
    )

    registry.register(
        "restore_window",
        "Restore a desktop window.",
        lambda target: handler.handle(
            "restore_window",
            target,
        ),
    )

    registry.register(
        "close_window",
        "Close a desktop window.",
        lambda target: handler.handle(
            "close_window",
            target,
        )
    )