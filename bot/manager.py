import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.main.handlers import router as main_router

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

    async def __send_message(self, telegram_id, text):
        await self.bot.send_message(telegram_id, text)

    async def test(self):
        await self.__send_message(787919997, "Извиняй мужык")
