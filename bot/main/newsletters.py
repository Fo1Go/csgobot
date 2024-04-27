import logging
from .parser import parse_news, parse_matches, parse_updates


async def get_matches() -> str | None:
    logging.log(level=logging.INFO, msg='Function \'get_matches\' is working')
    matches = parse_matches()
    msg = ''
    for match in matches:
        teams = match.team_names
        tournament = match.tournament_name
        info = match.match_info
        time = match.time_matches
        url_match = match.url_match
        url_analytics = match.url_analytic
        msg = msg + f'''{teams} in {time} at {tournament}
Match info: {info}
Url: {url_match}
Analytics: {url_analytics}
'''
    return msg if msg else None


async def get_update() -> str | None:
    update = parse_updates()
    return f'{update.update_date} {update.update_url}' if update else None


async def get_news() -> str | None:
    logging.log(level=logging.INFO, msg='Function \'get_news\' is working')
    news = parse_news()
    msg = ''
    for article in news:
        name = article.name
        url = article.url
        msg = msg + f'{name} {url}'
    return msg if msg else None
