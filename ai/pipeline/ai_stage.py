class AIStage:

    def __init__(self, brain):
        self.brain = brain


    def run(self, context):

        print("=" * 50)
        print("AI STAGE ENTERED")
        print("=" * 50)

        print("Decision:", context.decision)

        if context.decision is None:
            print("No decision")
            return

        if context.decision.route != "AI":
            print("Not AI route")
            return

        history = self.brain.chat_memory.recent()
        print("DEBUG: PASSED CHAT MEMORY")

        # -----------------------------
        # Knowledge Search
        # -----------------------------

        print("=" * 50)
        print("KNOWLEDGE SEARCH")
        print("QUERY:", context.input)
        print("=" * 50)

        knowledge = self.brain.knowledge_manager.search(
            context.input
        )

        if knowledge.success:

            print("=" * 50)
            print("KNOWLEDGE FOUND")
            print("SOURCE:", knowledge.source)
            print("CONFIDENCE:", knowledge.confidence)
            print("CONTENT:", knowledge.content)
            print("=" * 50)

            prompt = f"""
    User Question:
    {context.input}

    External Knowledge:
    {knowledge.content}

    Instructions:
    Use the external knowledge above as the primary factual source.
    Answer the user's question naturally and clearly.
    Do not mention the source unless necessary.
    Do not invent facts that are not supported by the knowledge.
    """

        else:

            print("=" * 50)
            print("NO KNOWLEDGE FOUND")
            print("ERROR:", knowledge.error)
            print("=" * 50)

            prompt = context.input

        # -----------------------------
        # Gemini
        # -----------------------------

        print("=" * 50)
        print("CALLING LLM")
        print("=" * 50)

        response = self.brain.llm.ask(
            prompt=prompt,
            history=history,
            name="User",
        )

        print("=" * 50)
        print("LLM RESPONSE")
        print(response)
        print("=" * 50)

        context.response = response
        context.stop = True