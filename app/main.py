from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.routers.free_games import free_games_router
from app.routers.free_loot import free_loot_router
from app.routers.platforms_menu import platforms_menu_router
from app.routers.utils import utils_router
from app.settings import settings


async def bot():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(utils_router, free_games_router, free_loot_router, platforms_menu_router)

    await dp.start_polling(bot)


app = run(bot())
