from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_keyboard():
    a = KeyboardButton(text='/author')
    h = KeyboardButton(text='/help')
    su = KeyboardButton(text='/subscribe_updates')
    uu = KeyboardButton(text='/unsubscribe_updates')
    sm = KeyboardButton(text='/subscribe_matches')
    um = KeyboardButton(text='/unsubscribe_matches')
    sn = KeyboardButton(text='/subscribe_news')
    un = KeyboardButton(text='/unsubscribe_news')
    mr = KeyboardButton(text='/matches_results')

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    kb.row(a, h)
    kb.row(su, uu)
    kb.row(sm, sm)
    kb.row(sn, un, mr)

    return kb
