from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_keyboard():
    a = KeyboardButton(text='/author')
    h = KeyboardButton(text='/help')
    s = KeyboardButton(text='/start')
    me = KeyboardButton(text='/me')
    m = KeyboardButton(text='/matches')
    n = KeyboardButton(text='/news')
    r = KeyboardButton(text='/results')
    u = KeyboardButton(text='/updates')

    keyboard = [
        [a, h, s],
        [me, r],
        [m, n, u]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
