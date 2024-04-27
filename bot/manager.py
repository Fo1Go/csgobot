import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.main.handlers import router as main_router
from bot.models import User
from bot.utils.db import session
from bot.main.newsletters import get_news, get_update, get_matches

load_dotenv("env")


class BotManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.token = os.getenv("CSGOBOT_TOKEN")
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        self.dp.include_router(main_router)

    async def start(self):
        try:
            await self.dp.start_polling(self.bot, skip_updates=True)
        except KeyboardInterrupt:
            print("Shutting down...")

    async def __send_message(self, telegram_id, text, turnoff_preview=True):
        await self.bot.send_message(telegram_id, text, disable_web_page_preview=turnoff_preview)

    async def send_matches_by_subscription(self):
        users = session.query(User).filter(User.subscribed_matches)
        msg = await get_matches()
        for user in users:
            await self.__send_message(user.telegram_id, msg)

    async def send_news_by_subscription(self):
        users = session.query(User).filter(User.subscribed_news)
        msg = await get_news()
        for user in users:
            await self.__send_message(user.telegram_id, msg)

    async def send_update_by_subscription(self):
        users = session.query(User).filter(User.subscribed_updates)
        msg = await get_update()
        for user in users:
            await self.__send_message(user.telegram_id, msg)
