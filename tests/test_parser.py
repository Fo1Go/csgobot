from bot.main.parser import parse_news, parse_matches, parse_results, parse_updates
from bot.main.dataclasses import Result, Match, Article
from bot.utils.parser import get_hltv_link, get_time, get_date, get_text
from bot.models import Update
from datetime import datetime
from mock import MockResponse


def test_parse_update(mocker):
    def mock_get_update_html(*args, **kwargs):
        return MockResponse().mock_get_updates(*args, **kwargs)

    mocker.patch('bot.main.parser.get_parser_object', mock_get_update_html)

    testing_update = parse_updates()
    expected_update = Update(update_date=datetime(2023, 2, 15),
                             update_url='https://blog.counter-strike.net/index.php/2023/02/41124/')
    assert testing_update.update_url == expected_update.update_url
    assert testing_update.update_date == expected_update.update_date


def test_parse_news(mocker):
    def mock_get_news_html(*args, **kwargs):
        return MockResponse().mock_get_news_html(*args, **kwargs)

    mocker.patch('bot.main.parser.get_parser_object', mock_get_news_html)

    testing_news = parse_news()
    testing_article = testing_news[0]
    expected_article = Article(
        name=get_text("Snappi on having no star player: \"There's a world where we can do it by committee\""),
        url=get_hltv_link("/news/38826/snappi-on-having-no-star-player-theres-a-world-where-we-can-do-it-by-committee"),
    )

    assert testing_article == expected_article


def test_parse_results(mocker):
    def mock_get_results_html(*args, **kwargs):
        return MockResponse().mock_get_results_html(*args, **kwargs)

    mocker.patch('bot.main.parser.get_parser_object', mock_get_results_html)

    testing_results = parse_results()
    testing_result = testing_results[0]
    expected_result = Result(
        team_names=get_text("Passion UA vs B8"),
        tournament_name=get_text("RES Regional Series 2 Europe"),
        match_result="0 - 2",
        url_match=get_hltv_link("/matches/2371395/passion-ua-vs-b8-res-regional-series-2-europe"),
    )
    assert testing_result == expected_result


def test_parse_matches(mocker):
    def mock_get_matches_html(*args, **kwargs):
        return MockResponse().mock_get_matches_html(*args, **kwargs)

    mocker.patch('bot.main.parser.get_parser_object', mock_get_matches_html)

    testing_matches = parse_matches()
    testing_match = testing_matches[0]
    expected_match = Match(
        time_matches=get_time(time="10:00"),
        match_info="bo3",
        team_names=get_text("Permitta vs ALTERNATE aTTaX"),
        tournament_name="European Pro League Season 15",
        url_match=get_hltv_link("/matches/2371289/permitta-vs-alternate-attax-european-pro-league-season-15"),
        url_analytic=get_hltv_link("/betting/analytics/2371289/permitta-vs-alternate-attax-european-pro-league-season"
                                   "-15"),
    )
    assert testing_match == expected_match
