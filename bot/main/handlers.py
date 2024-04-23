import asyncio
from aiogram import types
from bot.main.keyboard import create_keyboard
from routers import router
from bot.models import User

keyboard = create_keyboard()


@router.message_handler(commands=['start', 'help'])
async def start(
        message: types.Message
):
    msg = f"""
        Available commands:
        /subscribe_updates or /SU - Subscribe to news updates
        /unsubscribe_updates or /UU - Unsubscribe from news updates
        /subscribe_matches or /SM - Subscribe to matches
        /unsubscribe_matches or /UM - Unsubscribe from matches
        /subscribe_news or /SN - Subscribe to news
        /unsubscribe_news or /UN - Unsubscribe from news
        /matches_results - /MR Get matches result today"""
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['author'])
async def author(
        message: types.Message
):
    msg = """
        Github - https://github.com/Fo1Go
        Telegram - https://t.me/folgogo"""
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['subscribe_updates', 'SU'])
async def subscribe_updates(
        message: types.Message
):
    msg = "You subscribed on csgo updates news."
    db.update_subscription_updates(message.chat.id, True)
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['unsubscribe_updates', 'UU'])
async def unsubscribe_updates(
        message: types.Message
):
    msg = "You unsubscribe from csgo updates news."
    db.update_subscription_updates(message.chat.id, False)
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['subscribe_matches', 'SM'])
async def subscribe_matches(
    message: types.Message
):
    msg = "You subscribed on matches csgo."
    db.update_subscription_matches(message.chat.id, True)
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['unsubscribe_matches', 'UM'])
async def unsubscribe_matches(
    message: types.Message
):
    msg = "You unsubscribe from matches csgo."
    db.update_subscription_matches(message.chat.id, False)
    await message.answer(msg, reply_markup=keyboard)


@router.message_handler(commands=['subscribe_news', 'SN'])
async def subscribe_news(
    message: types.Message
):
    db.update_subscription_news(message.chat.id, True)
    await message.answer("You subscribed on news csgo.", reply_markup=keyboard)


@router.message_handler(commands=['unsubscribe_news', 'UN'])
async def unsubscribe_news(
    message: types.Message
):
    db.update_subscription_news(message.chat.id, False)
    await message.answer("You unsubscribed from news csgo.", reply_markup=keyboard)


@router.message_handler(commands=['matches_results', 'MR'])
async def matches_results(
    message: types.Message
):
    results = CSGOresult.get_result()
    result = ''
    if results[0]:
        teams = results[2]['teams']
        tournaments = results[2]['tournaments']
        scores = results[2]['scores']
        view = results[2]['view']
        url = results[2]['url']
        for i in range(len(teams)):
            wl = teams[i].split("|")
            team = ' \tVS\t '.join(teams[i].split("|"))
            result = (result
                      + f"Played {team}\nWon - {wl[0]}, Lose - {wl[1]} "
                      + f"\nFinally score - {scores[i]} in {view[i]} "
                      + f"\nTournament - {tournaments[i]}\nUrl on match - {url[i]}\n\n")
    await message.answer(f"{results[1]}\n\n{result}", reply_markup=keyboard)


async def get_matches(wait_for):
    print("Function \"get_matches\" is working")
    while True:
        await asyncio.sleep(wait_for)
        subscriptions = list(db.get_subscriptions_matches())
        matches = CSGOmatches.get_matches()
        result = ''
        if matches[0]:
            teams = matches[2]['teams']
            tournaments = matches[2]['tournament']
            time = matches[2]['time']
            view = matches[2]['view']
            url_match = matches[2]['url_match']
            url_analytics = matches[2]['url_analytics']

            for i in range(len(teams)):
                team = ' \tVS\t '.join(teams[i].split("|"))
                
                result = result +\
                    f"Play {team} in {time[i]}" +\
                    f"\nMatch meta - {view[i]} " +\
                    f"\nTournament - {tournaments[i]}" +\
                    f"\nUrl on match - {url_match[i]}" +\
                    f"\nUrl on analytics - {url_analytics[i]}\n\n"

            for i in range(len(subscriptions)):
                await myapibot.send_message(subscriptions[i][1], f"{matches[1]}\n\n{result}")


async def get_news(wait_for):
    print("Function \"get_news\" is working")
    while True:
        await asyncio.sleep(wait_for)
        result = []
        subscriptions = list(db.get_subscriptions_news())
        news = CSGOnews.get_news()
        if news[0]:
            for i in range(len(news[2]['name'])):
                msg = f"{news[1]}" +\
                    f"\n\n{news[2]['name'][i]}" +\
                    f"\n\n{news[2]['content'][i]}" +\
                    f"\nRead more:\n{news[2]['url'][i]}"
                result.append(msg)
            for i in range(len(subscriptions)):
                for a in range(len(result)):
                    res = result[a]
                    await myapibot.send_message(subscriptions[i][1], res)


async def get_updates(wait_for):
    print("Function \"get_updates\" is working")
    while True:
        await asyncio.sleep(wait_for)
        subscriptions = list(db.get_subscriptions_updates())
        update = CSGOupdate.get_updates()
        if update[0]:
            content = ''
            for i in update[1]['content']:
                content = content + i + "\n\n"
            result = f"{update[1]['name'][0]}" +\
                f"\n{update[1]['date'][0]}" +\
                f"\n\n{content}Read on blog csgo:\n{update[1]['url']}"
            for i in range(len(subscriptions)):
                await myapibot.send_message(subscriptions[i][1], result)
