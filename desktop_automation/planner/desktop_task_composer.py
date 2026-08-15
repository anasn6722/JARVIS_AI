from ai.agent.task import Task


class DesktopTaskComposer:
    """
    Compose deterministic desktop tasks from a natural-language
    desktop command.

    This layer handles common multi-step patterns while keeping
    execution deterministic and independent of the LLM.
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
        """

        if not text:
            return []

        text = str(text).strip()

        if not text:
            return []

        normalized = text.lower()

        # =====================================================
        # SIMPLE SEARCH COMMAND
        # =====================================================

        query = self._extract_search_query(text)

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

        if self._contains_open_search(normalized):
            typed_text = self._extract_type_text(text)

            if typed_text:
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

                if self._contains_enter(normalized):
                    tasks.append(
                        Task(
                            action="keyboard_press",
                            target="enter",
                        )
                    )

                return tasks

        return []

    # =========================================================
    # SEARCH QUERY
    # =========================================================

    def _extract_search_query(self, text):
        normalized = text.lower().strip()

        if not (
            normalized.startswith(
                self.SEARCH_PREFIXES
            )
        ):
            return ""

        if "google" in normalized:
            return ""

        for prefix in self.SEARCH_PREFIXES:
            if normalized.startswith(prefix):
                query = text[len(prefix):].strip()

                if query:
                    return query

        return ""

    # =========================================================
    # OPEN SEARCH
    # =========================================================

    @staticmethod
    def _contains_open_search(text):
        return any(
            phrase in text
            for phrase in (
                "open search",
                "open the search",
                "open search panel",
                "open the search panel",
                "open search view",
                "open the search view",
            )
        )

    # =========================================================
    # TYPE EXTRACTION
    # =========================================================

    @classmethod
    def _extract_type_text(cls, text):
        normalized = text.lower()
    
        marker = "type "
    
        index = normalized.find(marker)
    
        if index == -1:
            return ""
    
        value = text[index + len(marker):].strip()
    
        suffixes = (
            " and press enter",
            " then press enter",
            ", press enter",
            " press enter",
        )
    
        lower_value = value.lower()
    
        for suffix in suffixes:
            if lower_value.endswith(suffix):
                value = value[:-len(suffix)].strip()
                break
            
        # Remove a separator comma left before "and".
        value = value.rstrip(" ,")
    
        return value
    # =========================================================
    # PLAIN TYPE
    # =========================================================

    @classmethod
    def _extract_plain_type(cls, text):
        value = cls._extract_type_text(
            text
        )

        # "in Search" belongs to ui_type, not plain keyboard
        # typing.
        lower_value = value.lower()

        marker = " in "

        if marker in lower_value:
            index = lower_value.rfind(
                marker
            )

            value = value[:index].strip()

        return value

    # =========================================================
    # ENTER DETECTION
    # =========================================================

    @staticmethod
    def _contains_enter(text):
        return (
            "press enter" in text
            or "then enter" in text
            or "and enter" in text
        )