from ai.prompt import build_prompt


class ConversationBuilder:
    

    def build(
        self,
        system_prompt,
        history,
        prompt,
    ):

        conversation = [
            system_prompt
        ]

        if history:

            for item in history:

                conversation.append(
                    f"{item['speaker']}: {item['message']}"
                )

        conversation.append(
            f"User: {prompt}"
        )

        return conversation