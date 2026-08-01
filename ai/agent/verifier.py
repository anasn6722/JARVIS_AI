class AgentVerifier:

    def verify(self, task, response):

        if response is None:
            return False

        if not isinstance(response, str):
            return False

        response = response.strip()

        if not response:
            return False

        lower = response.lower()

        failure_keywords = (
            "failed",
            "error",
            "exception",
            "not found",
            "couldn't",
            "cannot",
            "can't",
            "unable",
            "invalid",
            "no application",
            "no website",
        )

        if any(word in lower for word in failure_keywords):
            return False

        return True