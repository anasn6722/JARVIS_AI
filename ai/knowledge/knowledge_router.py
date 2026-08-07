from ai.knowledge.knowledge_result import KnowledgeResult


class KnowledgeRouter:

    def __init__(self, sources):

        self.sources = sources


    def search(self, query):

        best = None


        for source in self.sources:

            try:

                result = source.search(query)


                if not result:
                    continue


                if result.success:

                    return result


                if best is None:

                    best = result


            except Exception as e:

                print(
                    f"{source.name} failed:",
                    e
                )


        return best or KnowledgeResult(

            success=False,

            source="",

            query=query,

            content="",

            confidence=0.0,

        )