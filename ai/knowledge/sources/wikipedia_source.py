import wikipedia

from ai.knowledge.models.knowledge_result import KnowledgeResult
from ai.knowledge.sources.base import KnowledgeSource


class WikipediaSource(KnowledgeSource):

    @property
    def name(self):
        return "Wikipedia"

    def search(self, query):

        try:

            summary = wikipedia.summary(
                query,
                sentences=3,
                auto_suggest=False,
            )

            return KnowledgeResult(

                success=True,

                source="Wikipedia",

                query=query,

                content=summary,

                confidence=0.95,
            )

        except wikipedia.DisambiguationError as e:

            return KnowledgeResult(

                success=True,

                source="Wikipedia",

                query=query,

                content=f"Did you mean: {', '.join(e.options[:5])}?",

                confidence=0.6,
            )

        except wikipedia.PageError:

            return KnowledgeResult(

                success=False,

                source="Wikipedia",

                query=query,

                content="",

                confidence=0.0,
            )

        except Exception as e:
            print("=" * 60)
            print("WIKIPEDIA ERROR")
            print(type(e).__name__)
            print(e)
            print("=" * 60)
        
            return KnowledgeResult(
                success=False,
                source="Wikipedia",
                query=query,
                content="",
            )