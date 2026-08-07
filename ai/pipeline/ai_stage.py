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


        # -----------------------------
        # Knowledge Search
        # -----------------------------

        knowledge = self.brain.knowledge_manager.search(
            context.input
        )


        if knowledge.success:

            print("=" * 50)
            print("KNOWLEDGE FOUND")
            print("SOURCE:", knowledge.source)
            print("=" * 50)


            prompt = f"""

User Question:
{context.input}


External Knowledge:
{knowledge.content}


Instructions:
Use the knowledge above.
Answer naturally.
Do not mention Wikipedia unless needed.
Do not invent information.

"""


        else:

            print("=" * 50)
            print("NO KNOWLEDGE FOUND")
            print("=" * 50)


            prompt = context.input



        # -----------------------------
        # Gemini
        # -----------------------------

        print("Calling LLM...")


        response = self.brain.llm.ask(

            prompt=prompt,

            history=history,

            name="User",

        )


        print("LLM Response:", response)


        context.response = response

        context.stop = True