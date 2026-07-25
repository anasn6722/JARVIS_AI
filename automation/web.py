import webbrowser


class WebController:

    def open_url(self, url: str):
        webbrowser.open(url)