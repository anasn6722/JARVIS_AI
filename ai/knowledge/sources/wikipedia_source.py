import re

import requests

from ai.knowledge.models.knowledge_result import KnowledgeResult
from ai.knowledge.sources.base import KnowledgeSource


class WikipediaSource(KnowledgeSource):
    """Retrieve knowledge from Wikipedia."""

    BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"

    @property
    def name(self):
        return "Wikipedia"

    def _clean_query(self, query: str) -> str:
        """Convert a natural-language question into a Wikipedia title."""

        cleaned = query.strip()

        prefixes = [
            r"^what is\s+",
            r"^what are\s+",
            r"^who is\s+",
            r"^who was\s+",
            r"^where is\s+",
            r"^where was\s+",
            r"^when was\s+",
            r"^when did\s+",
            r"^tell me about\s+",
            r"^explain\s+",
            r"^describe\s+",
        ]

        for pattern in prefixes:
            cleaned = re.sub(
                pattern,
                "",
                cleaned,
                flags=re.IGNORECASE,
            )

        cleaned = cleaned.rstrip("?!.")

        return cleaned.strip()

    def search(self, query: str):
        """Search Wikipedia's REST API."""

        cleaned_query = self._clean_query(query)

        if not cleaned_query:
            return KnowledgeResult(
                success=False,
                source=self.name,
                query=query,
                content="",
                confidence=0.0,
                error="Empty Wikipedia query",
            )

        try:
            url = (
                f"{self.BASE_URL}/"
                f"{requests.utils.quote(cleaned_query)}"
            )

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "JARVIS-AI/1.0",
                    "Accept": "application/json",
                },
            )

            if response.status_code == 404:
                return KnowledgeResult(
                    success=False,
                    source=self.name,
                    query=query,
                    content="",
                    confidence=0.0,
                    error="Wikipedia page not found",
                )

            response.raise_for_status()

            data = response.json()

            summary = data.get("extract", "")

            if not summary:
                return KnowledgeResult(
                    success=False,
                    source=self.name,
                    query=query,
                    content="",
                    confidence=0.0,
                    error="Wikipedia returned no summary",
                )

            return KnowledgeResult(
                success=True,
                source=self.name,
                query=query,
                content=summary,
                confidence=0.95,
            )

        except requests.RequestException as error:
            return KnowledgeResult(
                success=False,
                source=self.name,
                query=query,
                content="",
                confidence=0.0,
                error=str(error),
            )

        except ValueError as error:
            return KnowledgeResult(
                success=False,
                source=self.name,
                query=query,
                content="",
                confidence=0.0,
                error=f"Invalid JSON response: {error}",
            )

        except Exception as error:
            return KnowledgeResult(
                success=False,
                source=self.name,
                query=query,
                content="",
                confidence=0.0,
                error=str(error),
            )