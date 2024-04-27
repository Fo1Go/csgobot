from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_keyboard():
    # s = KeyboardButton(text='/start')

    a = KeyboardButton(text='/author')
    h = KeyboardButton(text='/help')
    me = KeyboardButton(text='/me')

    u = KeyboardButton(text='/updates')
    m = KeyboardButton(text='/matches')
    n = KeyboardButton(text='/news')
    r = KeyboardButton(text='/results')

    us = KeyboardButton(text='/updates_sub')
    ms = KeyboardButton(text='/matches_sub')
    ns = KeyboardButton(text='/news_sub')

    keyboard = [
        [me, h],
        [r, m, n, u],
        [ns, ms, us],
        [a]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
