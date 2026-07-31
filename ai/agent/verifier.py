class AgentVerifier:

    def verify(self, task, response):

        if response is None:
            return False

        if response == "":
            return False

        if isinstance(response, str):

            lower = response.lower()

            if "couldn't" in lower:
                return False

            if "not found" in lower:
                return False

            if "failed" in lower:
                return False

        return True