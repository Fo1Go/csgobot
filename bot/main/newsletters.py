import asyncio
from .parser import parse_news, parse_matches, parse_updates
from bot.utils.db import session
from bot.models import User


async def send_matches():
    print('Function \'send_matches\' is working')
    subscriptions = session.query(User).filter(User.subscribed_matches)
    matches = parse_matches()
    msg = ''
    for match in matches:
        teams = match.team_names
        tournaments = match.tournament_name
        info = match.match_info
        time = match.time_matches
        url_match = match.url_match
        url_analytics = match.url_analytic
        for i in range(len(teams)):
            msg = msg + \
                f'''{teams} in {time} at {tournaments[i]}
                Match info: {info}
                Url: {url_match}
                Analytics: {url_analytics}
                '''
        # for user in subscriptions:
        #     await bot.send_message(user.telegram_id, msg)


# async def get_news(wait_for):
#     print('Function \'get_news\' is working')
#     while True:
#         await asyncio.sleep(wait_for)
#         result = []
#         subscriptions = list(db.get_subscriptions_news())
#         news = CSGOnews.get_news()
#         if news[0]:
#             for i in range(len(news[2]['name'])):
#                 msg = f'{news[1]}' + \
#                       f'\n\n{news[2]['name'][i]}' + \
#                       f'\n\n{news[2]['content'][i]}' + \
#                       f'\nRead more:\n{news[2]['url'][i]}'
#                 result.append(msg)
#             for i in range(len(subscriptions)):
#                 for a in range(len(result)):
#                     res = result[a]
#                     await myapibot.send_message(subscriptions[i][1], res)
#
#
# async def get_updates(wait_for):
#     print('Function \'get_updates\' is working')
#     while True:
#         await asyncio.sleep(wait_for)
#         subscriptions = list(db.get_subscriptions_updates())
#         update = CSGOupdate.get_updates()
#         if update[0]:
#             content = ''
#             for i in update[1]['content']:
#                 content = content + i + '\n\n'
#             result = f'{update[1]['name'][0]}' + \
#                      f'\n{update[1]['date'][0]}' + \
#                      f'\n\n{content}Read on blog csgo:\n{update[1]['url']}'
#             for i in range(len(subscriptions)):
#                 await myapibot.send_message(subscriptions[i][1], result)
