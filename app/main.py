from asyncio import run

from aiogram import Bot, Dispatcher

from app.routers.test import test_router
from app.routers.free_games import free_games_router
from app.routers.categories_menu import categories_menu_router
from app.routers.utils import utils_router
from app.settings import settings


async def bot():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(utils_router, test_router, free_games_router, categories_menu_router)

    await dp.start_polling(bot)


app = run(bot())
