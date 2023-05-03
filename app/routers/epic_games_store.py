from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.GAb_API import GAbAPI

egs_router = Router()


@egs_router.message(Command("get_current_games"))
async def get_current_epic_games(message: Message):

    async with GAbAPI() as api:
        responce = await api.get_current_epic_games()

    await message.answer(str(responce))


@egs_router.message(Command("get_next_games"))
async def get_next_epic_games(message: Message):

    async with GAbAPI() as api:
        responce = await api.get_next_epic_games()

    await message.answer(str(responce))
