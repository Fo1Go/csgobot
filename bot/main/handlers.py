from aiogram.types import LinkPreviewOptions

from bot.main.routers import router
from aiogram import types, F
from aiogram.filters.command import Command
from bot.main.keyboard import create_keyboard
from bot.utils.db import session
from bot.utils.utils import get_user_by_id, yes_or_no, un_or_noting, get_or_create_user
from bot.main.parser import parse_results
from bot.main.newsletters import get_update, get_matches, get_news


keyboard = create_keyboard()


@router.message(Command('help'))
async def helping(
        message: types.Message
):
    msg = f'''Available commands:
/start - register in the bot
/help - see all available commands
/author - author contacts
/me - get information about me
/update - toggle subscription CSGO updates
/matches - toggle subscription CSGO matches
/news - toggle subscription CSGO news
/results - get matches results for this day
'''
    await message.answer(msg, reply_markup=keyboard)


@router.message(Command('start'))
async def start(
        message: types.Message
):
    get_or_create_user(telegram_id=message.from_user.id)
    msg = 'Enter /help to see all available commands'
    await message.answer(msg, reply_markup=keyboard)


@router.message(Command('me'))
async def me(
        message: types.Message
):
    user = get_user_by_id(telegram_id=message.from_user.id)
    msg = f'''
Hi @{message.from_user.username}!
Your subscriptions:
News: {yes_or_no(user.subscribed_news)}
Matches: {yes_or_no(user.subscribed_matches)}
Updates: {yes_or_no(user.subscribed_updates)}'''
    await message.answer(msg, reply_markup=keyboard)


@router.message(Command('author'))
async def author(
        message: types.Message
):
    msg = '''Github - https://github.com/Fo1Go
Telegram - https://t.me/folgogo'''
    await message.answer(msg, reply_markup=keyboard, link_preview_options=LinkPreviewOptions(is_disabled=True))


@router.message(Command('updates'))
async def updates(
        message: types.Message
):
    update = await get_update()
    if update is None:
        update = 'No new news'
    await message.answer(update, reply_markup=keyboard)


@router.message(Command('matches'))
async def matches(
        message: types.Message
):
    matches_today = await get_matches()
    if matches_today is None:
        matches_today = 'No matches today'
    await message.answer(matches_today, reply_markup=keyboard)


@router.message(Command('news'))
async def view_news(
        message: types.Message
):
    news_today = await get_news()
    if news_today is None:
        news_today = 'No news today'
    await message.answer(news_today, reply_markup=keyboard)


@router.message(Command('results'))
async def results(
        message: types.Message
):

    matches_results = parse_results()
    for match in matches_results:
        msg = f'''{match.team_names} 
played {match.match_result} 
at {match.tournament_name}
URL: {match.url_match}'''
        await message.answer(msg, reply_markup=keyboard)


@router.message(Command('updates_sub'))
async def updates(
        message: types.Message
):
    user = get_user_by_id(telegram_id=message.from_user.id)
    if user is not None:
        msg = f'You {un_or_noting(user.subscribed_updates)}subscribed on matches csgo.'
        user.subscribed_updates = not user.subscribed_updates
        session.commit()
        await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer('Unknown user', reply_markup=keyboard)


@router.message(Command('matches_sub'))
async def matches(
        message: types.Message
):
    user = get_user_by_id(telegram_id=message.from_user.id)
    if user is not None:
        msg = f'You {un_or_noting(user.subscribed_matches)}subscribed on matches csgo.'
        user.subscribed_matches = not user.subscribed_matches
        session.commit()
        await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer('Unknown user', reply_markup=keyboard)


@router.message(Command('news_sub'))
async def news(
        message: types.Message
):
    user = get_user_by_id(telegram_id=message.from_user.id)
    if user is not None:
        msg = f'You {un_or_noting(user.subscribed_news)}subscribed on news csgo.'
        user.subscribed_news = not user.subscribed_news
        session.commit()
        await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer('Unknown user', reply_markup=keyboard)


@router.message(F.photo)
async def photo(
        message: types.Message
):
    msg = 'Зачем фотку отправил?'
    await message.answer(msg, reply_markup=keyboard)
