import webbrowser
from urllib.parse import quote


class WebController:
    def open_url(self, url: str):
        webbrowser.open(url)

    def google_search(self, query: str):
        url = (
            "https://www.google.com/search?q="
            + quote(query)
        )
        webbrowser.open(url)

    def youtube_search(self, query: str):
        url = (
            "https://www.youtube.com/results?search_query="
            + quote(query)
        )
        webbrowser.open(url)