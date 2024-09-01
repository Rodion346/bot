import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.routes.generate_img_clot import router, bot
from bot.routes.bot import start_router
from bot.routes.generate_img_simple import simple_router
from bot.routes.get_fef_money import router_get_money
from bot.routes.top_balance import router_balance

dp = Dispatcher()

storage = MemoryStorage()

dp.include_router(router)
dp.include_router(start_router)
dp.include_router(simple_router)
dp.include_router(router_balance)
dp.include_router(router_get_money)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())