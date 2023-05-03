from asyncio import run

from aiogram import Bot, Dispatcher

from app.routers.test import test_router
from app.routers.epic_games_store import egs_router
from app.settings import settings


async def bot():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(test_router, egs_router)

    await dp.start_polling(bot)


app = run(bot())
