from .dataclasses import Article, Match, Result
from bot.models import Update
from bot.utils.db import session
from bot.utils.parser import get_time, get_text, get_parser_object, get_date, get_hltv_link


def parse_news() -> list[Article]:
    url = 'https://www.hltv.org/'
    news = list()
    parser = get_parser_object(url)
    raw_articles = parser.find('div', {"class": "standard-box standard-list"})
    html_articles = raw_articles.find_all('a', {"class": "article"})
    for html_article in html_articles:
        article = Article(
            name=get_text(html_article.find('div', {'class': 'newstext'})),
            url=get_hltv_link(html_article.get('href'))
        )
        news.append(article)
    return news


def parse_matches() -> list[Match]:
    url = 'https://www.hltv.org/matches'
    matches = list()
    parser = get_parser_object(url)

    raw_matches = parser.find('div', {"class": "upcomingMatchesSection"})
    html_matches = raw_matches.find_all('div', {'class': 'upcomingMatch'})

    for html_match in html_matches:
        match = Match(
            time_matches=get_time(get_text(html_match.find('div', {'class': 'matchTime'}))),
            match_info=get_text(html_match.find('div', {'class': 'matchMeta'})),
            team_names=' vs '.join(map(get_text, html_match.find_all('div', {'class': 'matchTeamName'}))),
            tournament_name=get_text(html_match.find('div', {'class': 'matchEventName'})),
            url_match=get_hltv_link(str(html_match.find('a', {'class': 'match a-reset'}).get('href'))),
            url_analytic=get_hltv_link(str(html_match.find('a', {'class': 'matchAnalytics'}).get('href')))
        )
        matches.append(match)
    return matches


def parse_results() -> list[Result]:
    url = 'https://www.hltv.org/results'
    results = list()
    parser = get_parser_object(url)

    raw_results = parser.find_all('div', {"class": "results-sublist"})[0]
    html_results = raw_results.find_all('div', {'class': 'result-con'})
    for html_result in html_results:
        result = Result(
            team_names=' vs '.join(map(get_text, html_result.find_all('td', {'class': 'team-cell'}))),
            tournament_name=get_text(html_result.find('span', {'class': 'event-name'})),
            match_result=get_text(html_result.find('td', {'class': 'result-score'})),
            url_match=get_hltv_link(str(html_result.find('a', {'class': 'a-reset'}).get('href')))
        )
        results.append(result)
    return results


def parse_updates() -> Update | None:
    url = 'https://blog.counter-strike.net/index.php/category/updates/'
    parser = get_parser_object(url)
    last_update = parser.find('div', {"class": "inner_post"})
    last_date_update = get_date(last_update.find('p', {'class': 'post_date'}))
    if not session.query(Update).filter(Update.update_date == last_date_update).first():
        update = Update(
            update_url=last_update.find('h2').find('a').get("href"),
            update_date=last_date_update
        )
        session.add(update)
        session.flush()
        return update
    return None
