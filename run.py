from bot.manager import BotManager
import asyncio


if __name__ == "__main__":
    bot = BotManager()
    asyncio.run(bot.start())
