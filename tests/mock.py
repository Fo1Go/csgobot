from pathlib import Path
from bs4 import BeautifulSoup


class MockResponse:
    path = Path('D:\\information\\csgobot\\tests\\files')

    @staticmethod
    def mock_get_news_html():
        # html get from site https://www.hltv.org/
        with open(MockResponse.path / "news.html", "r") as f:
            return BeautifulSoup(markup=f.read(), features='html.parser')

    @staticmethod
    def mock_get_results_html():
        # html get from site https://www.hltv.org/results
        with open(MockResponse.path / "results.html", "r") as f:
            return BeautifulSoup(markup=f.read(), features='html.parser')

    @staticmethod
    def mock_get_matches_html():
        # html get from site https://www.hltv.org/matches
        with open(MockResponse.path / "matches.html", "r") as f:
            return BeautifulSoup(markup=f.read(), features='html.parser')

    @staticmethod
    def mock_get_updates():
        # html get from site https://blog.counter-strike.net/index.php/category/updates
        with open(MockResponse.path / "update.html", "r") as f:
            return BeautifulSoup(markup=f.read(), features='html.parser')
