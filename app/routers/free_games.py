from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.Games_API import GamesAPI

free_games_router = Router()


@free_games_router.message(Command("get_free_games"))
async def get_free_games(message: Message) -> None:

    async with GamesAPI() as api:
        responce = await api.get_all_free_games()

    print(str(responce))

    # await message.answer(str(responce))


@free_games_router.message(Command("get_free_games_by_platform"))
async def get_free_games_by_platform(message: Message) -> None:

    platform = "".join(message.text.split()[1:])  # type: ignore

    async with GamesAPI() as api:
        responce = await api.get_free_games_by_platform(platform)

    print(str(responce))

    await message.answer(str(responce))
