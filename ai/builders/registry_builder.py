from ai.commands import CommandRegistry


class RegistryBuilder:

    @staticmethod
    def build(brain):

        registry = CommandRegistry()

        # -------------------------
        # Built-in
        # -------------------------

        registry.register(
            "hello",
            lambda command: brain.builtin.hello()
        )

        registry.register(
            "identity",
            lambda command: brain.builtin.identity()
        )

        registry.register(
            "time",
            lambda command: brain.builtin.time()
        )

        # -------------------------
        # Search
        # -------------------------

        registry.register(
            "search",
            brain.handle_search,
        )

        registry.register(
            "youtube",
            brain.handle_youtube,
        )

        # -------------------------
        # Apps
        # -------------------------

        registry.register(
            "open",
            brain.app_handler.open,
        )

        # -------------------------
        # Memory
        # -------------------------

        registry.register(
            "set_preference",
            brain.handle_set_preference,
        )

        registry.register(
            "get_preference",
            brain.handle_get_preference,
        )

        registry.register(
            "last_message",
            brain.handle_last_message,
        )

        registry.register(
            "history",
            brain.handle_history,
        )

        registry.register(
            "set_name",
            brain.handle_set_name,
        )

        registry.register(
            "get_name",
            brain.handle_get_name,
        )

        # -------------------------
        # Goals
        # -------------------------

        registry.register(
            "add_goal",
            brain.handle_add_goal,
        )

        registry.register(
            "show_goals",
            brain.handle_show_goals,
        )

        registry.register(
            "next_task",
            brain.handle_next_task,
        )

        registry.register(
            "complete_task",
            brain.handle_complete_task,
        )

        registry.register(
            "goal_progress",
            brain.handle_goal_progress,
        )

        registry.register(
            "delete_goal",
            brain.handle_delete_goal,
        )

        return registry