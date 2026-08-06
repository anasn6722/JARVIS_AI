class ResponseParser:

    def parse(self, response):

        if response is None:

            return ""

        return str(response).strip()