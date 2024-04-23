import logging
from aiogram import Bot, Dispatcher, types
from .main.routers import router as main_router
import os
from dotenv import load_dotenv

load_dotenv("env_file")


class BotManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.token = os.getenv("CSGOBOT_TOKEN")
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()

    async def start(self):
        self.dp.include_router(main_router)
        await self.dp.start_polling(self.bot, skip_updates=True)

