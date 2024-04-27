import logging

from bot.manager import BotManager
import asyncio
from typing import Callable

bot_object = BotManager()


async def wait_until_and_run(time_in_seconds=1, function:  Callable = None, *args, **kwargs):
    logging.log(level=logging.INFO, msg=f'\'{function.__name__}\' will done in {time_in_seconds} seconds')
    await asyncio.sleep(time_in_seconds)
    if function:
        await function(*args, **kwargs)


async def on_startup():
    logging.log(level=logging.INFO, msg="Startup starts")
    while True:
        await wait_until_and_run(time_in_seconds=15, function=bot_object.send_news_by_subscription)
        await wait_until_and_run(time_in_seconds=15, function=bot_object.send_matches_by_subscription)
        await wait_until_and_run(time_in_seconds=15, function=bot_object.send_update_by_subscription)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup())
    loop.create_task(bot_object.start())
    loop.run_forever()
