from ai.agent.task import Task


class DesktopTaskComposer:
    """
    Compose deterministic desktop tasks from natural-language
    desktop commands.

    This layer handles common multi-step desktop patterns while
    keeping execution deterministic and independent of the LLM.
    """

    SEARCH_PREFIXES = (
        "search for ",
        "search ",
    )

    TYPE_IN_MARKER = " in "

    OPEN_SEARCH_PHRASES = (
        "open search",
        "open the search",
        "open search panel",
        "open the search panel",
        "open search view",
        "open the search view",
    )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def compose(self, text):
        """
        Return a list of deterministic desktop Tasks.

        Examples:

            open search and type Python
                -> search_ui("Python")

            open search, type Python, and press enter
                -> search_ui("Python")

            search for Python tutorials
                -> search_ui("Python tutorials")

            type hello world and press enter
                -> keyboard_type("hello world")
                -> keyboard_press("enter")

            find File and click it
                -> ui_find_descriptor("File")
                -> ui_click_descriptor("$LAST_UI")

            find File, click it, then find Explorer and click it
                -> ui_find_descriptor("File")
                -> ui_click_descriptor("$LAST_UI")
                -> ui_find_descriptor("Explorer")
                -> ui_click_descriptor("$LAST_UI")
        """

        if not text:
            return []

        text = str(text).strip()

        if not text:
            return []

        normalized = text.lower().strip()

        # =====================================================
        # FIND + CLICK UI CHAIN
        # =====================================================

        ui_tasks = self._compose_find_click_chain(
            text
        )

        if ui_tasks:
            return ui_tasks

        # =====================================================
        # SIMPLE SEARCH COMMAND
        # =====================================================

        query = self._extract_search_query(
            text
        )

        if query:
            return [
                Task(
                    action="search_ui",
                    target=query,
                )
            ]

        # =====================================================
        # OPEN SEARCH + TYPE
        # =====================================================

        if self._contains_open_search(
            normalized
        ):
            typed_text = self._extract_type_text(
                text
            )

            if typed_text:
                # search_ui is already atomic:
                # open/focus/type/submit are handled internally.
                return [
                    Task(
                        action="search_ui",
                        target=typed_text,
                    )
                ]

            return [
                Task(
                    action="keyboard_hotkey",
                    target="ctrl+shift+f",
                )
            ]

        # =====================================================
        # TYPE + ENTER
        # =====================================================

        if normalized.startswith("type "):
            typed_text = self._extract_plain_type(
                text
            )

            if typed_text:
                tasks = [
                    Task(
                        action="keyboard_type",
                        target=typed_text,
                    )
                ]

                if self._contains_enter(
                    normalized
                ):
                    tasks.append(
                        Task(
                            action="keyboard_press",
                            target="enter",
                        )
                    )

                return self._sequence(
                    tasks
                )

        return []

    # =========================================================
    # FIND + CLICK COMPOSITION
    # =========================================================

    def _compose_find_click_chain(self, text):
        """
        Compose semantic UI find/click sequences.

        Supported forms:

            find File and click it
            find File, click it
            find File then click it

            find File, click it, then find Explorer and click it
        """

        segments = self._split_ui_sequence(
            text
        )

        if not segments:
            return []

        tasks = []

        index = 0

        while index < len(segments):

            current = segments[index].strip()

            if not current:
                index += 1
                continue

            # -------------------------------------------------
            # FIND COMMAND
            # -------------------------------------------------

            if self._starts_with_find(
                current
            ):
                name = self._extract_find_target(
                    current
                )

                if not name:
                    return []

                tasks.append(
                    Task(
                        action="ui_find_descriptor",
                        target=name,
                    )
                )

                index += 1

                # -------------------------------------------------
                # FOLLOWING CLICK COMMAND
                # -------------------------------------------------

                if index < len(segments):
                    next_segment = segments[
                        index
                    ].strip()

                    if self._is_click_current(
                        next_segment
                    ):
                        tasks.append(
                            Task(
                                action="ui_click_descriptor",
                                target="$LAST_UI",
                            )
                        )

                        index += 1

                continue

            # -------------------------------------------------
            # IGNORE STANDALONE CLICK-IT
            # -------------------------------------------------

            if self._is_click_current(
                current
            ):
                # A standalone "click it" has no known context
                # unless a previous find created LAST_UI.
                tasks.append(
                    Task(
                        action="ui_click_descriptor",
                        target="$LAST_UI",
                    )
                )

                index += 1
                continue

            return []

        # Require at least one semantic UI task.
        if not tasks:
            return []

        # At least one find task must exist.
        if not any(
            task.action
            == "ui_find_descriptor"
            for task in tasks
        ):
            return []

        return self._sequence(
            tasks
        )

    # =========================================================
    # UI SEQUENCE SPLITTING
    # =========================================================

    @staticmethod
    def _split_ui_sequence(text):
        """
        Split UI action chains on explicit sequence markers.

        Examples:

            find File and click it
                -> ["find File", "click it"]

            find File, click it, then find Explorer and click it
                -> [
                    "find File",
                    "click it",
                    "find Explorer",
                    "click it",
                ]
        """

        normalized = str(text).strip()

        if not normalized:
            return []

        # Normalize commas surrounding "then".
        normalized = normalized.replace(
            ", then ",
            " then ",
        )

        # Explicit "then" is always a safe boundary here.
        parts = [
            part.strip()
            for part in normalized.split(
                " then "
            )
            if part.strip()
        ]

        result = []

        for part in parts:

            # Split "find X and click it".
            lower = part.lower()

            marker = " and click"

            if marker in lower:
                index = lower.find(
                    marker
                )

                left = part[
                    :index
                ].strip()

                right = part[
                    index + len(" and "):
                ].strip()

                if left:
                    result.append(
                        left
                    )

                if right:
                    result.append(
                        right
                    )

                continue

            # Split comma-separated UI steps.
            comma_parts = [
                value.strip()
                for value in part.split(",")
                if value.strip()
            ]

            result.extend(
                comma_parts
            )

        return result

    # =========================================================
    # FIND HELPERS
    # =========================================================

    @staticmethod
    def _starts_with_find(text):
        """Return True when a segment starts with find/locate."""

        normalized = text.lower().strip()

        return (
            normalized.startswith("find ")
            or normalized.startswith("locate ")
        )

    @staticmethod
    def _extract_find_target(text):
        """Extract the semantic UI target from a find command."""

        value = text.strip()

        normalized = value.lower()

        prefixes = (
            "find ",
            "locate ",
        )

        for prefix in prefixes:
            if normalized.startswith(
                prefix
            ):
                target = value[
                    len(prefix):
                ].strip()

                # Remove harmless trailing click wording.
                suffixes = (
                    " and click it",
                    " and click",
                )

                lower_target = target.lower()

                for suffix in suffixes:
                    if lower_target.endswith(
                        suffix
                    ):
                        target = target[
                            :-len(suffix)
                        ].strip()
                        break

                return target.rstrip(" ,")

        return ""

    @staticmethod
    def _is_click_current(text):
        """
        Return True for commands referring to the previously
        discovered UI element.
        """

        normalized = text.lower().strip()

        return normalized in {
            "click it",
            "click",
            "press it",
            "activate it",
        }

    # =========================================================
    # SEARCH QUERY
    # =========================================================

    def _extract_search_query(self, text):
        """Extract a desktop search query."""

        normalized = text.lower().strip()

        if not normalized.startswith(
            self.SEARCH_PREFIXES
        ):
            return ""

        # Do not intercept Google/web searches.
        if "google" in normalized:
            return ""

        for prefix in self.SEARCH_PREFIXES:
            if normalized.startswith(prefix):
                query = text[
                    len(prefix):
                ].strip()

                query = query.rstrip(" ,")

                if query:
                    return query

        return ""

    # =========================================================
    # OPEN SEARCH
    # =========================================================

    @classmethod
    def _contains_open_search(cls, text):
        """Return True when the command refers to desktop Search."""

        return any(
            phrase in text
            for phrase in cls.OPEN_SEARCH_PHRASES
        )

    # =========================================================
    # TYPE EXTRACTION
    # =========================================================

    @classmethod
    def _extract_type_text(cls, text):
        """Extract text following 'type'."""

        normalized = text.lower()

        marker = "type "

        index = normalized.find(
            marker
        )

        if index == -1:
            return ""

        value = text[
            index + len(marker):
        ].strip()

        suffixes = (
            " and press enter",
            " then press enter",
            ", press enter",
            " press enter",
        )

        lower_value = value.lower()

        for suffix in suffixes:
            if lower_value.endswith(
                suffix
            ):
                value = value[
                    :-len(suffix)
                ].strip()
                break

        value = value.rstrip(" ,")

        return value

    # =========================================================
    # PLAIN TYPE
    # =========================================================

    @classmethod
    def _extract_plain_type(cls, text):
        """
        Extract text for ordinary keyboard typing.

        Example:
            type hello world and press enter
            -> hello world
        """

        value = cls._extract_type_text(
            text
        )

        if not value:
            return ""

        lower_value = value.lower()

        marker = " in "

        if marker in lower_value:
            index = lower_value.rfind(
                marker
            )

            value = value[
                :index
            ].strip()

        return value

    # =========================================================
    # TASK SEQUENCING
    # =========================================================

    @staticmethod
    def _sequence(tasks):
        """
        Make composed tasks execute sequentially.

        The first task has no dependency.
        Every later task depends on the immediately previous task.
        """

        if not tasks:
            return []

        for index in range(
            1,
            len(tasks),
        ):
            previous = tasks[
                index - 1
            ]

            current = tasks[
                index
            ]

            current.depends_on = [
                previous.id
            ]

        return tasks

    # =========================================================
    # ENTER DETECTION
    # =========================================================

    @staticmethod
    def _contains_enter(text):
        """Return True when the command requests Enter."""

        return (
            "press enter" in text
            or "then enter" in text
            or "and enter" in text
        )