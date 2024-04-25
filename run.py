from bot.manager import BotManager
import asyncio


bot_object = BotManager()


async def on_startup():
    print("Startup starts")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup())
    loop.create_task(bot_object.start())
    loop.run_forever()
